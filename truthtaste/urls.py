from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import delete_review

app_name = 'truthtaste'

urlpatterns = [
    path('list/', views.restaurant_list_list, name='all_restaurant_list'),
    path('<int:store_id>', views.restaurant_detail, name='restaurant-detail'),
    path('', views.home, name='home'),
    # path('auth/sign-up-page', views.signup_page, name='sign-up-page'),
    path('add-restaurant/', views.add_restaurant, name='add-restaurant'),
    path('edit-restaurant/<int:box_id>/', views.edit_restaurant, name='edit-restaurant'),
    path('delete-restaurant/<int:box_id>/', views.delete_restaurant, name='delete-restaurant'),
    path('create-review/', views.create_review, name='create-review'),
    path('delete-review/<int:review_id>/', delete_review, name='delete-review'),
    path('edit-review/<int:review_id>/', views.edit_review, name='edit-review'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
