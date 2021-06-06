import time
from django.core.paginator import Paginator
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from slugify import slugify
from engine.settings import dotenv_path
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, date

load_dotenv(dotenv_path)


def get_datetime_in_sec(start: datetime, end: datetime) -> list:
    start_date = int(datetime.timestamp(start))
    end_date = int(datetime.timestamp(end))

    return [{"start": start_date, "end": end_date}]


def create_paginator(query_set: list, obj_per_page: int, request: HttpRequest, query=None) -> tuple:
    paginator = Paginator(query_set, obj_per_page)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if query:
        params = f'?query={query}&page='

    else:
        params = '?page='

    if page.has_previous():
        prev_url = params + str(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = params + str(page.next_page_number())
    else:
        next_url = ''

    return page, prev_url, next_url, is_paginated


def generate_slug(title):
    return slugify(title)


def get_coordinates(address):
    base_url = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'format': 'json',
        'apikey': os.environ.get('API_KEY'),
        'geocode': 'Москва, ' + address
    }

    response = requests.get(base_url, params=params)

    if response:
        data = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        coordinates = data.split(' ')

        return {'lat': coordinates[1], 'lon': coordinates[0]}

    else:
        print('Произошла ошибка при попытке получить ответ. Код ответа ' + str(response.status_code))


class ObjectUpdateMixin:
    form_title = None
    model = None
    template = None

    def get(self, request, slug):
        retrieved_obj = self.model.objects.get(slug=slug)
        bound_form = self.form_title(instance=retrieved_obj)

        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): retrieved_obj})

    def post(self, request, slug):
        retrieved_obj = self.model.objects.get(slug=slug)
        bound_form = self.form_title(request.POST, instance=retrieved_obj)

        if bound_form.is_valid():
            updated_obj = bound_form.save()
            return redirect(updated_obj)

        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): retrieved_obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        obj = self.model.objects.get(slug=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))


class ObjectSearchingMixin:
    form = None
    template_get = None
    template_post = None
    model = None

    def get(self, request):
        form_obj = self.form()
        return render(request, self.template_get, context={'form': form_obj})

    def post(self, request):
        bound_form = self.form(request.POST)

        if bound_form.is_valid():
            events_list = []
            user_date = bound_form.cleaned_data['date']
            place = bound_form.cleaned_data['place']
            old_events = self.model.objects.filter(place=place)

            for event in old_events:
                for date_ in event.dates:
                    try:
                        if date.fromtimestamp(date_['start']) <= user_date <= date.fromtimestamp(date_['end']):
                            events_list.append(event)
                    except OSError:
                        if date_['start'] <= int(time.mktime(user_date.timetuple())) <= date_['end']:
                            events_list.append(event)

            if not events_list:
                raise Http404

            page_obj, prev_page, next_page, is_paginated = create_paginator(list(set(events_list)), 5, request)
            context = {
                'page': page_obj,
                'prev_page': prev_page,
                'next_page': next_page,
                'is_paginated': is_paginated,
                'flag': True,
                'date': user_date,
                'place_obj': bound_form.cleaned_data['place']
            }

            return render(request, self.template_post, context=context)

        return render(request, self.template_get, context={'form': bound_form})