from django import forms
from .models import *
from django.core.exceptions import ValidationError


class SubwayForm(forms.ModelForm):
    class Meta:
        model = Subway
        fields = ['name']
        labels = {'name': 'Название станции'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-2'})
        }

    def clean_name(self):
        new_station = self.cleaned_data['name'].capitalize()

        if Subway.objects.filter(name__iexact=new_station).count():
            raise ValidationError("Станция метро с таким названием уже существует.")

        return new_station


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Название категории'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-2'})
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']
        labels = {'title': 'Название тега'}
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-2'})
        }


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ['slug', 'coordinates']
        labels = {
            'title': 'Название',
            'description': 'Краткое описание',
            'body_text': 'Описание',
            'address': 'Адрес',
            'schedule': 'Расписание',
            'phone': 'Телефон',
            'subway': 'Метро',
            'site': 'Сайт',
            'photo': 'Фото',
            'category': 'Категория',
            'tags': 'Теги'
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-2'}),
            'body_text': forms.Textarea(attrs={'class': 'form-control mt-2'}),
            'address': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'schedule': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'phone': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'subway': forms.SelectMultiple(attrs={'class': 'form-control mt-2'}),
            'site': forms.URLInput(attrs={'class': 'form-control mt-2'}),
            'photo': forms.URLInput(attrs={'class': 'form-control mt-2'}),
            'category': forms.Select(attrs={'class': 'form-control mt-2'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control mt-2'})
        }


class EventForm(forms.ModelForm):
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control mt-2', 'type': 'datetime-local'}),
        label='Дата начала')

    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control mt-2', 'type': 'datetime-local'}),
        label='Дата окончания')

    class Meta:
        model = Events
        exclude = ['slug', 'dates']
        labels = {
            'title': 'Название',
            'description': 'Краткое описание',
            'body_text': 'Описание',
            'age_restriction': 'Возрастное ограничение',
            'photo': 'Фото',
            'price': 'Цена',
            'tags': 'Теги',
            'place': 'Место проведения'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'description': forms.Textarea(attrs={'class': 'form-control mt-2'}),
            'body_text': forms.Textarea(attrs={'class': 'form-control mt-2'}),
            'age_restriction': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'photo': forms.URLInput(attrs={'class': 'form-control mt-2'}),
            'price': forms.TextInput(attrs={'class': 'form-control mt-2'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control mt-2'}),
            'place': forms.Select(attrs={'class': 'form-control mt-2'})
        }


class SearchingByArchiveForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control mt-2', 'type': 'date'}), label='Дата')
    place = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control mt-2'}), label='Место',
                                   queryset=Place.objects.all(), empty_label='Место не выбрано')


class SearchingEventsForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control mt-2', 'type': 'date'}), label='Дата')
    place = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control mt-2'}), label='Место',
                                   queryset=Place.objects.all(), empty_label='Место не выбрано')