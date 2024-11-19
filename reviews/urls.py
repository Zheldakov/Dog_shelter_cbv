from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import ReviewListView, DeactivatedDogReviewListView, ReviewDetailView, ReviewUpdateView, \
    ReviewDeleteView, ReviewCreateView, review_toggle_activity

app_name = ReviewsConfig.name  # for backwards compatibility

urlpatterns = [

    path('', ReviewListView.as_view(), name='list_reviews'),
    path('review/deactivated/', DeactivatedDogReviewListView.as_view(), name='deactivated_reviews_list'),
    path('review/create/', ReviewCreateView.as_view(), name='create_review'),
    path('review/detail/<slug:slug>/', ReviewDetailView.as_view(), name='detail_review'),
    path('review/update/<slug:slug>/', ReviewUpdateView.as_view(), name='create_update_review'),
    path('review/delete/<slug:slug>/', ReviewDeleteView.as_view(), name='delete_review'),
    path('review/toggle/<slug:slug>/', review_toggle_activity, name='review_toggle_activity'),
]
