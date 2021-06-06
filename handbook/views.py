from datetime import datetime
from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import View
from itertools import chain
from .services import generate_slug, get_coordinates, create_paginator, ObjectUpdateMixin, get_datetime_in_sec, \
    ObjectDeleteMixin, ObjectSearchingMixin
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .management.commands._private import add_to_history


def subway_list(request):
    stations = Subway.objects.all()
    page_obj, prev_page, next_page, is_paginated = create_paginator(stations, 30, request)

    context = {
        'page': page_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated
    }
    return render(request, 'handbook/subway_list.html', context=context)


def get_associated_with_station_places(request, slug):
    subway = Subway.objects.get(slug=slug)
    places = Place.objects.filter(subway__slug__contains=slug)
    page_obj, prev_page, next_page, is_paginated = create_paginator(places, 5, request)

    context = {
        'page': page_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated,
        'subway': subway,
        'admin_panel': subway,
        'not_delete': True
    }

    return render(request, 'handbook/objects_list.html', context=context)


def rubric_choice(request):
    rubrics = Category.objects.all()
    return render(request, 'handbook/rubrics_list.html', context={"rubrics": rubrics})


def objects_list(request, slug):
    rubric_obj = Category.objects.get(slug=slug)
    places = Place.objects.filter(category=rubric_obj)
    page_obj, prev_page, next_page, is_paginated = create_paginator(places, 5, request)

    context = {
        'page': page_obj,
        'rubric': rubric_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated,
        'admin_panel': rubric_obj,
        'not_delete': True
    }

    return render(request, 'handbook/objects_list.html', context=context)


def place_detail(request, slug):
    place_obj = Place.objects.get(slug=slug)

    return render(request, 'handbook/place_detail.html',
                  context={'record': place_obj, 'admin_panel': place_obj, 'detail': True})


def get_query_result(request):
    search_query = request.GET['query']

    if not search_query:
        raise Http404('An empty request was passed.')

    response = list(chain(Place.objects.filter(title__icontains=search_query),
                          Events.objects.filter(title__icontains=search_query)))

    if not response:
        raise Http404("No matches found.")

    page_obj, prev_page, next_page, is_paginated = create_paginator(response, 5, request, search_query)

    context = {
        'page': page_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated,
        'query': search_query
    }
    return render(request, 'handbook/objects_list.html', context=context)


def get_associated_with_tag_objects(request, slug):
    tag_obj = Tag.objects.get(slug=slug)
    objects = list(set(chain(Place.objects.filter(tags__slug__contains=slug),
                             Events.objects.filter(tags__slug__contains=slug))))

    page_obj, prev_page, next_page, is_paginated = create_paginator(objects, 5, request)

    context = {
        'page': page_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated,
        'tag': tag_obj,
        'objects': '' if not objects else objects,
        'admin_panel': tag_obj,
        'detail': True
    }

    return render(request, 'handbook/objects_list.html', context=context)


def tags_list(request):
    tags = Tag.objects.all()
    page_obj, prev_page, next_page, is_paginated = create_paginator(tags, 30, request)

    context = {
        'page': page_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated
    }

    return render(request, 'handbook/tags_list.html', context=context)


def event_detail(request, slug):
    event_obj = Events.objects.get(slug=slug)
    passed_events_dates = None

    if History.objects.filter(slug=slug).count():
        passed_events_dates = History.objects.get(slug=slug).dates

    return render(request, 'handbook/event_detail.html',
                  context={'record': event_obj, 'admin_panel': event_obj,
                           'old_events': passed_events_dates, 'add_to_archive': True})


def add_to_archive(request, slug):
    event = Events.objects.get(slug=slug)
    place = event.place
    add_to_history(event)
    event.delete()

    return redirect(place)


def passed_event_detail(request, slug):
    old_event = History.objects.get(slug=slug)

    return render(request, 'handbook/event_detail.html', context={'record': old_event})


def passed_events_list(request):
    curr_date = int(datetime.timestamp(datetime.now()))
    events = Events.objects.filter(dates__0__end__lt=curr_date).order_by('title')

    if not events:
        raise Http404

    page_obj, prev_page, next_page, is_paginated = create_paginator(events, 5, request)
    context = {
        'page': page_obj,
        'prev_page': prev_page,
        'next_page': next_page,
        'is_paginated': is_paginated,
        'old_events_list': True
    }

    return render(request, 'handbook/objects_list.html', context=context)


@login_required(login_url='/admin')
def create_metro_station(request):
    if request.method == 'GET':
        subway_form = SubwayForm()

        return render(request, 'handbook/create_metro_station.html', context={'subway_form': subway_form})

    bound_form = SubwayForm(request.POST)

    if bound_form.is_valid():
        bound_form.save()
        return redirect('rubrics_list', permanent=True)

    return render(request, 'handbook/create_metro_station.html', context={'subway_form': bound_form})


@login_required(login_url='/admin')
def create_place(request):
    if request.method == 'GET':
        place_form = PlaceForm()

        return render(request, 'handbook/create_place.html', context={'place_form': place_form})

    bound_form = PlaceForm(request.POST)

    if bound_form.is_valid():
        new_place = bound_form.save(commit=False)
        new_place.slug = generate_slug(new_place.title)

        if new_place.address:
            new_place.coordinates = get_coordinates(new_place.address)
        new_place.save()
        bound_form.save_m2m()
        return redirect('place_description', new_place.slug)

    return render(request, 'handbook/create_place.html', context={'place_form': bound_form})


@login_required(login_url='/admin')
def create_category(request):
    if request.method == 'GET':
        category_form = CategoryForm()

        return render(request, 'handbook/create_category.html', context={'category_form': category_form})

    bound_form = CategoryForm(request.POST)

    if bound_form.is_valid():
        new_category = bound_form.save(commit=False)
        new_category.slug = generate_slug(new_category.name)
        new_category.save()
        return redirect('rubrics_list', permanent=True)

    return render(request, 'handbook/create_category.html', context={'category_form': bound_form})


@login_required(login_url='/admin')
def create_tag(request):
    if request.method == 'GET':
        tag_form = TagForm()

        return render(request, 'handbook/create_tag.html', context={'tag_form': tag_form})

    bound_form = TagForm(request.POST)

    if bound_form.is_valid():
        new_tag = bound_form.save(commit=False)
        new_tag.slug = generate_slug(new_tag.title)
        new_tag.save()
        return redirect('tags_list', permanent=True)

    return render(request, 'handbook/create_tag.html', context={'tag_form': bound_form})


@login_required(login_url='/admin')
def create_event(request):
    if request.method == 'GET':
        event_form = EventForm()

        return render(request, 'handbook/create_event.html', context={'event_form': event_form})

    bound_form = EventForm(request.POST)

    if bound_form.is_valid():
        new_event = bound_form.save(commit=False)
        new_event.slug = generate_slug(new_event.title)
        new_event.dates = get_datetime_in_sec(bound_form.cleaned_data['start'], bound_form.cleaned_data['end'])
        new_event.save()
        bound_form.save_m2m()
        return redirect(new_event)

    return render(request, 'handbook/create_event.html', context={'event_form': bound_form})


class UpdatePlace(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_title = PlaceForm
    model = Place
    template = 'handbook/edit_place.html'
    login_url = '/admin'


class UpdateTag(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_title = TagForm
    model = Tag
    template = 'handbook/edit_tag.html'
    login_url = '/admin'


class UpdateCategory(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_title = CategoryForm
    model = Category
    template = 'handbook/edit_rubric.html'
    login_url = '/admin'


class UpdateEvent(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_title = EventForm
    model = Events
    template = 'handbook/edit_event.html'
    login_url = '/admin'


class UpdateMetroStation(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_title = SubwayForm
    model = Subway
    template = 'handbook/edit_metro_station.html'
    login_url = '/admin'


class DeleteEvent(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Events
    template = 'handbook/delete_event.html'
    redirect_url = 'rubrics_list'
    login_url = '/admin'


class DeleteTag(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'handbook/delete_tag.html'
    redirect_url = 'tags_list'
    login_url = '/admin'


class DeletePlace(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Place
    template = 'handbook/delete_place.html'
    redirect_url = 'rubrics_list'
    login_url = '/admin'


class SearchingByArchive(ObjectSearchingMixin, View):
    form = SearchingByArchiveForm
    template_get = 'handbook/searching_by_archive_form.html'
    template_post = 'handbook/objects_list.html'
    model = History


class SearchingEvents(ObjectSearchingMixin, View):
    form = SearchingEventsForm
    template_get = 'handbook/searching_events_form.html'
    template_post = 'handbook/objects_list.html'
    model = Events
