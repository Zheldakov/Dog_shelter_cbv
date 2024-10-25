import datetime

from django import forms

from dogs.models import Dog
from users.forms import StyleFromMixin

class DogForm(StyleFromMixin,forms.ModelForm):
    # Создаем форму для добавления/редактирования питомца с указанными полями
    class Meta:
        model = Dog
        exclude = ('owner',)

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        if cleaned_data is None:
            return None
        now_year = datetime.datetime.now().year
        if now_year - cleaned_data.year >100:
            raise forms.ValidationError('Возраст питомца не может быть больше 100 лет')
        return cleaned_data
