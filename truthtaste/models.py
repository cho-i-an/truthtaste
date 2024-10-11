from datetime import datetime
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

from djangoProject import settings


# Restaurant
class StoreBox(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurant/')
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('truthtaste:restaurant-detail', args=[self.id])


# Reviews
class Review(models.Model):
    store = models.ForeignKey(StoreBox, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=50)


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150)
#     newsletter_subscription = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.username

# class StoreBox:
#     def __init__(self, id, title, score, type, description, image):
#         self.id = id
#         self.title = title
#         self.score = score
#         self.type = type
#         self.description = description
#         self.image = image
#         # self.url = url


# box1 = StoreBox(
#     1,
#     "Riverside Roasters",
#     "4.5 (123)",
#     "Coffee shop",
#     "Freshly roasted beans paired with homemade desserts.",
#     "images/restaurant/restaurant-1.jpg"
# )
#
# box2 = StoreBox(
#     2,
#     "Sunrise Sips Café",
#     "4.3 (96)",
#     "Coffee shop",
#     "Rustic cafe offering organic blends & baked goods.",
#     "images/restaurant/restaurant-2.jpg"
# )
#
# box3 = StoreBox(
#     3,
#     "Daily Drip Coffeehouse",
#     "4.1 (215)",
#     "Coffee shop",
#     "Coffee oasis with an emphasis on sustainable practices.",
#     "images/restaurant/restaurant-3.jpg"
# )
#
# box4 = StoreBox(
#     4,
#     "Blue Cup Coffee",
#     "4.3 (96)",
#     "Coffee shop",
#     "Contemporary café serving both classic and experimental brews.",
#     "images/restaurant/restaurant-4.jpg"
# )
#
# box5 = StoreBox(
#     5,
#     "Leaf & Bean Lounge",
#     "4.5 (54)",
#     "Coffee shop",
#     "Every coffee bean tells a story of sustainability and care.",
#     "images/restaurant/restaurant-5.jpg"
# )
#
# box6 = StoreBox(
#     6,
#     "Blue Cup Coffee",
#     "4.5 (154)",
#     "Coffee shop",
#     "Embracing nature's serenity one brew at a time.",
#     "images/restaurant/restaurant-6.jpg"
# )
#
# box7 = StoreBox(
#     7,
#     "Twilight Espresso Longe",
#     "4.1 (133)",
#     "Coffee shop",
#     "Indulge in coffee as the city lights dim, a perfect blend of night and caffeine.",
#     "images/restaurant/restaurant-7.jpg"
# )
#
# box8 = StoreBox(
#     8,
#     "Canvas Coffee Gallery",
#     "4.4 (199)",
#     "Coffee shop",
#     "Where art and aroma create an enthralling masterpiece.",
#     "images/restaurant/restaurant-8.jpg"
# )
#
# store_boxes = []
# store_boxes.append(box1)
# store_boxes.append(box2)
# store_boxes.append(box3)
# store_boxes.append(box4)
# store_boxes.append(box5)
# store_boxes.append(box6)
# store_boxes.append(box7)
# store_boxes.append(box8)

regular_user = {"username": "Rick", "password": "regular"}
admin_user = {"username": "Emily", "password": "admin"}