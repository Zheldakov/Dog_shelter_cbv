from django.urls import path

from reviews.apps import ReviewsConfig
from reviews.views import CategoryReviewListView, DeactivatedDogReviewListView

app_name = ReviewsConfig.name  # for backwards compatibility

urlpatterns = [

    path('<int:pk>/reviews/',CategoryReviewListView.as_view(), name='reviews_list'),
    path('<int:pk>/reviews/deactivated/',DeactivatedDogReviewListView.as_view(), name='deactivated_reviews_list'),
]