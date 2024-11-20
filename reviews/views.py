from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.shortcuts import reverse, get_object_or_404, redirect
from django.views.generic import CreateView, CreateView, DeleteView, UpdateView, ListView
from django.core.exceptions import PermissionDenied

from reviews.models import Review
from users.models import UserRoles
from reviews.forms import ReviewForm
from reviews.utils import slug_generation


class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Питомник - Все отзывы по собаке'
    }
    template_name = 'reviews/reviews.html'

    def get_queryset(self):
        queryset = super().queryset()
        # queryset = queryset.filter(dog_pk=self.kwargs.get('pk'))
        queryset = queryset.filter(sign_of_review=True)

        return queryset


class DeactivatedDogReviewListView(LoginRequiredMixin, ListView):
    model = Review
    extra_context = {
        'title': 'Неактивные отзывы'
    }
    template_name = 'reviews/reviews.html'

    def get_queryset(self):
        queryset = super().queryset()
        queryset = queryset.filter(dog_pk=self.kwargs.get('pk'))
        queryset = queryset.filter(sign_of_review=False)

        return queryset


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name ='reviews/review_create_review.html'

class ReviewDetailView(LoginRequiredMixin,DeleteView):
    model = Review
    template_name ='reviews/review_detail.html'

class ReviewUpdateView(LoginRequiredMixin,DeleteView):
    model = Review
    form_class = ReviewForm
    template_name ='reviews/review_create_update.html'

    def form_valid(self,form):
        if self.request.user.role not in [UserRoles.USER, UserRoles.ADMIN]:
            return HttpResponseForbidden()
        self.object = form.save()
        print(self.object.slug)
        if self.object.slug == "temp_slug":
            self.object.slug = slug_generation()
            print(self.object.slug)
        self.object.autor =self.request.user
        self.object.save()
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('reviews:detail_review', args=[self.kwargs.get('slug')])

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.autor != self.request.user and self.request.user not in [UserRoles.ADMIN, UserRoles.MODERATOR]:
            raise PermissionDenied()
        return self.object

class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    model = Review
    template_name ='reviews/review_delete.html'
    permission_required = 'reviews.delete_review'

    def get_success_url(self):
        return reverse('reviews:list_reviews')


def review_toggle_activity(request, sjug):
    review_item = get_object_or_404(Review, slug=sjug)
    if review_item.sign_of_review:
        review_item.sign_of_review = False
        review_item.save()
        return redirect(reverse('reviews:deactivated_reviews'))
    else:
        review_item.sign_of_review = True
        review_item.save()
        return redirect(reverse('reviews:list_reviews'))
