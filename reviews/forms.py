from django import forms
from reviews.models import Review
from dogs.forms import StyleFromMixin


class ReviewForm(StyleFromMixin, forms.ModelForm):
    # Создаем форму для добавления/редактирования отзыва с указанными полями
    title=forms.CharField(max_length=150,label='Заголовок_формы')
    content=forms.TextInput()
    slug=forms.SlugField(max_length=20, initial='temp_slug', widget=forms.HiddenInput())
    class Meta:
        model = Review
        fields = ('dog','title','content','slug')
