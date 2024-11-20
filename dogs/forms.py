import datetime

from django import forms

from dogs.models import Dog, Parent
from users.forms import StyleFromMixin


class DogForm(StyleFromMixin, forms.ModelForm):
    # Создаем форму для добавления/редактирования питомца с указанными полями
    class Meta:
        model = Dog
        exclude = ('owner', 'is_active', 'views')

    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        if cleaned_data is None:
            return None
        now_year = datetime.datetime.now().year
        if now_year - cleaned_data.year > 100:
            raise forms.ValidationError(
                'Возраст питомца не может быть больше 100 лет')
        return cleaned_data


class DogAdminForm(StyleFromMixin, forms.ModelForm):
    class Meta:
        model = Dog
        exclude = '__all__'

    # @staticmethod
    # def clean_birth_date():
    #     DogForm.clean_birth_date()
    def clean_birth_date(self):
        cleaned_data = self.cleaned_data['birth_date']
        if cleaned_data is None:
            return None
        now_year = datetime.datetime.now().year
        if now_year - cleaned_data.year > 100:
            raise forms.ValidationError(
                'Возраст питомца не может быть больше 100 лет')
        return cleaned_data


class ParentForm(StyleFromMixin, forms.ModelForm):
    # Создаем форму для добавления/редактирования родителя с указанными полями
    class Meta:
        model = Parent
        fields = '__all__'
