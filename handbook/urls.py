from django.urls import path
from .views import *


urlpatterns = [
    path('search/', get_query_result, name='objects_searching'),
    path('tags/', tags_list, name='tags_list'),
    path('tag/create/', create_tag, name='create_tag'),
    path('tag/<slug:slug>/', get_associated_with_tag_objects, name='tag_objects'),
    path('tag/<slug:slug>/edit/', UpdateTag.as_view(), name='edit_tag'),
    path('tag/<slug:slug>/delete/', DeleteTag.as_view(), name='delete_tag'),
    path('rubrics/', rubric_choice, name='rubrics_list'),
    path('rubric/create/', create_category, name='create_category'),
    path('rubric/<slug:slug>/', objects_list, name='objects_list'),
    path('rubric/<slug:slug>/edit/', UpdateCategory.as_view(), name='update_rubric'),
    path('place/create/', create_place, name='create_place'),
    path('place/<slug:slug>/', place_detail, name='place_description'),
    path('place/<slug:slug>/edit/', UpdatePlace.as_view(), name='edit_place'),
    path('place/<slug:slug>/delete/', DeletePlace.as_view(), name='delete_place'),
    path('event/create/', create_event, name='create_event'),
    path('event/<slug:slug>/', event_detail, name='event_description'),
    path('event/<slug:slug>/edit/', UpdateEvent.as_view(), name='edit_event'),
    path('event/<slug:slug>/delete/', DeleteEvent.as_view(), name='delete_event'),
    path('event/<slug:slug>/add_to_archive/', add_to_archive, name='add_to_archive_url'),
    path('subway/create/', create_metro_station, name='create_station'),
    path('subway/', subway_list, name='subway_list'),
    path('subway/<slug:slug>/', get_associated_with_station_places, name='subway_places'),
    path('subway/<slug:slug>/edit/', UpdateMetroStation.as_view(), name='edit_station'),
    path('searching_by_archive/', SearchingByArchive.as_view(), name='searching_by_archive_url'),
    path('passed_event/<slug:slug>/', passed_event_detail, name='old_event_url'),
    path('passed_events_list/', passed_events_list, name='passed_events_list_url'),
    path('searching_events/', SearchingEvents.as_view(), name='searching_events_url')
]