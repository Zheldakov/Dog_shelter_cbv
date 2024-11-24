from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import ReviewListView, DeactivatedDogReviewListView, ReviewDetailView, ReviewUpdateView, \
    ReviewDeleteView, ReviewCreateView, review_toggle_activity

app_name = ReviewsConfig.name  # for backwards compatibility

urlpatterns = [

    path('', ReviewListView.as_view(), name='list_reviews'),
    path('reviews/deactivated/', DeactivatedDogReviewListView.as_view(), name='deactivated_reviews_list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='create_review'),
    path('reviews/detail/<slug:slug>/', ReviewDetailView.as_view(), name='detail_review'),
    path('reviews/update/<slug:slug>/', ReviewUpdateView.as_view(), name='create_update_review'),
    path('reviews/delete/<slug:slug>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('reviews/toggle/<slug:slug>/', review_toggle_activity, name='toggle_activity_review'),
]
