from datetime import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import regular_user, admin_user, StoreBox, Review, User
from django.db.models import Avg, Value, FloatField
from django.db.models.functions import Coalesce
from actions.models import Action
from django.views.decorators.http import require_http_methods


def home(request):
    if request.session.get("username", False):  # Logged in
        # Feeds
        actions = Action.objects.all().order_by('-created')[:5]
        return render(request, "truthtaste/dashboard.html", {"actions": actions})
    else:
        return render(request, "truthtaste/home.html")


# List of all restaurant
def restaurant_list_list(request):
    sort_by = request.GET.get('sort_by', 'title_asc')

    # Use Coalesce to set the default average rating to 0 (If no ratings)
    store_boxes = StoreBox.objects.annotate(
        average_rating=Coalesce(Avg('reviews__rating'), Value(0), output_field=FloatField())
    )

    if sort_by == 'title_asc':
        store_boxes = store_boxes.order_by('title')
    elif sort_by == 'title_desc':
        store_boxes = store_boxes.order_by('-title')
    elif sort_by == 'score':
        store_boxes = store_boxes.order_by('-average_rating', 'title')
    else:
        store_boxes = store_boxes.order_by('type')

    actions = Action.objects.all().order_by('-created')[:5]
    context = {
        'store_boxes': store_boxes,
        "sort_by": sort_by,
        "actions": actions
    }

    return render(request,
                  "truthtaste/restaurant_list/restaurant-list.html", context)


# Detail of the restaurant
def restaurant_detail(request, store_id):
    store = get_object_or_404(StoreBox, id=store_id)
    reviews = store.reviews.all().order_by('-date')

    # Calculate the average rating if there are reviews
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is not None:
        average_rating = round(average_rating, 1)

    actions = Action.objects.all().order_by('-created')[:5]
    context = {
        'store': store,
        'reviews': reviews,
        'average_rating': average_rating,
        "actions": actions
    }
    return render(request, 'truthtaste/restaurant_list/restaurant-detail.html', context)


# For adding a new restaurant
def add_restaurant(request):
    if not request.session.get("username", False):
        messages.error(request, 'Only login users can add restaurants')
        return redirect('truthtaste:home')

    if request.method == 'POST':
        title = request.POST.get('add-title')
        type = request.POST.get('add-type')
        description = request.POST.get('add-description')
        image = request.FILES.get('add-image', None)

        user = User.objects.get(username=request.session.get("username"))

        ns = StoreBox(
            title=title,
            type=type,
            description=description,
            # author=user
            author=request.session['username']
        )
        if image:
            ns.image = image
        ns.save()

        # Log the action
        action = Action(
            user=user,
            verb="created the restaurant",
            target=ns,
        )
        action.save()

        messages.success(request, "You have successfully added the restaurant: %s." % ns.title,
                         extra_tags='success-add')
        # Redirect to the detail view for the new item
        return redirect('truthtaste:restaurant-detail', store_id=ns.id)
    else:
        return render(request, 'truthtaste/add-restaurant.html')


# For editing a restaurant
def edit_restaurant(request, box_id):
    # Check if user is logged in
    if not request.session.get("username"):
        messages.error(request, 'Only login users can edit the restaurant.')
        return redirect('truthtaste:home')
    try:
        box = StoreBox.objects.get(id=box_id)
    except StoreBox.DoesNotExist:
        messages.error(request, 'The restaurant does not exist!')
        return redirect('truthtaste:all_restaurant_list')

    if request.method == 'POST':
        user = User.objects.get(username=request.session.get("username"))
        title = request.POST.get('add-title')
        type = request.POST.get('add-type')
        description = request.POST.get('add-description')
        image = request.FILES.get('add-image', None)

        if title and title != box.title:
            box.title = title
            action = Action(
                user=user,
                verb="edited the restaurant title",
                target=box,
            )
            action.save()

        if description and description != box.description:
            box.description = description
            action = Action(
                user=user,
                verb="edited the restaurant description",
                target=box,
            )
            action.save()

        if type:
            box.type = type
        if image:
            box.image = image

        box.save()
        messages.success(request, "The restaurant %s was edited successfully!" % box.title, extra_tags='success-edit')
        return redirect('truthtaste:restaurant-detail', store_id=box.id)

    context = {
        'box': box,
    }
    return render(request, 'truthtaste/edit-restaurant.html', context)


# For deleting a restaurant
def delete_restaurant(request, box_id):
    user = get_object_or_404(User, username=request.session.get("username"))
    try:
        box = StoreBox.objects.get(id=box_id)
        box_title_deleted = box.title

        action = Action(
            user=user,
            verb="deleted a restaurant",
            details=f": {box_title_deleted}"
        )
        action.save()
        box.delete()
        messages.success(request, 'The restaurant %s was deleted successfully!' % box.title,
                         extra_tags='success-delete')
    except StoreBox.DoesNotExist:
        messages.error(request, 'The restaurant does not exist.')
    return redirect('truthtaste:all_restaurant_list')


def signup_page(request):
    messages.error(request, 'The registration feature is still in the development stage.')
    return render(request, "truthtaste/auth/sign-up-page.html")


def create_review(request):
    print("create_review")
    # print(request.body)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == "POST":
        try:
            store_id = int(request.POST.get('store_id'))
            title = request.POST.get('title')
            content = request.POST.get('content')
            rating = request.POST.get('rating')
            author = request.session.get('username')
            date = datetime.now()

            review = Review(
                store=StoreBox.objects.get(id=store_id),
                date=date,
                title=title,
                content=content,
                rating=rating,
                author=author,
            )
            print(review)
            review.save()

            can_edit = (author == request.session.get('username')) or request.user.is_superuser

            messages.success(request, "Your review was created successfully!")
            return JsonResponse(
                {'success': 'success', 'message': 'Successfully added a new review.', 'title': title, 'rating': rating
                    , 'content': content, 'author': author, 'can_edit': can_edit,
                 'review_id': review.id
                 }, status=200)
            # return redirect('truthtaste:restaurant-detail', store_id=store.id)
        except Review.DoesNotExist:
            return JsonResponse({'error': 'No store found for this ID'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid Ajax request'}, status=400)


# @require_http_methods(["DELETE"])
def delete_review(request, review_id):
    print("Delete review request received")
    review = get_object_or_404(Review, id=review_id)

    if review.author == request.session.get('username') or request.session.get('role') == 'admin':
        review.delete()
        messages.success(request, 'Review successfully deleted.')
        return redirect('truthtaste:restaurant-detail', store_id=review.store.id)
    else:
        messages.error(request, 'Permission denied')
        return redirect('truthtaste:restaurant-detail', review_id=review.store.id)


def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.author != request.session.get('username') and request.session.get('role') != 'admin':
        messages.error(request, 'You do not have permission to edit reviews.')
        return redirect('truthtaste:restaurant-detail', store_id=review.store.id)

    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.content = request.POST.get('content')
        review.rating = request.POST.get('rating')
        review.save()

        messages.success(request, 'Reviews successfully edited!')
        return redirect('truthtaste:restaurant-detail', store_id=review.store.id)
    else:
        return render(request, 'truthtaste/edit-review.html', {'review': review})