import requests
from handbook.models import *
from slugify import slugify
import time

created = 0
common_fields = ("title", "slug", "description", "body_text", "images")
base_url = "https://kudago.com/public-api/v1.4/"
common_params = {
    "location": "msk",
    "text_format": "text"
}


def get_json(url, data):
    """Получение данных с сервера в формате json"""

    response = requests.get(url, params=data)
    return response.json()["results"]


def get_metro_station(place, station):
    """Получение станций метро для конкретного места"""
    if not station:
        return

    elif "," in station:
        temp_list = station.split(",")
        for title in temp_list:
            station_name = Subway.objects.get_or_create(
                slug=slugify(title.strip()),
                defaults={
                    "name": title.strip(),
                    "slug": slugify(title)
                }
            )
            place.subway.add(station_name[0])

    else:
        station_name = Subway.objects.get_or_create(
            slug=slugify(station),
            defaults={
                "name": station,
                "slug": slugify(station)
            }
        )
        place.subway.add(station_name[0])


def get_category(category):
    """Получение категории для места"""

    rubric = Category.objects.get(slug=category)
    return rubric


def get_tags(obj, tags):
    """Получение тегов для места или события"""
    for tag in tags:
        instance = Tag.objects.get_or_create(
            slug=slugify(tag),
            defaults={
                "title": tag,
                "slug": slugify(tag)
            }
        )

        obj.tags.add(instance[0])


def get_actual_dates(dates):
    """
    Получение актуальных дат для события
    :param dates: даты для события, которое пришло из json
    :return: актуальные даты для события
    """

    actual_dates = []  # отфильтрованные актуальные даты из json

    now = int(time.time())
    for date in dates:
        if date["start"] >= now <= date["end"] \
                or date["start"] <= now <= date["end"]:
            actual_dates.append({
                "start": date["start"],
                "end": date["end"]
            })

        else:
            continue

    return actual_dates


def add_to_history(past_event, old_dates=None):
    """Добавление в историю прошедших событий"""

    old_event, is_created = History.objects.get_or_create(
        slug=past_event.slug,
        defaults=(
            dict(title=past_event.title,
                 slug=past_event.slug,
                 description=past_event.description,
                 body_text=past_event.body_text,
                 dates=old_dates if old_dates else past_event.dates,
                 age_restriction=past_event.age_restriction,
                 photo=past_event.photo,
                 price=past_event.price,
                 tags_list=[tag for tag in past_event.tags.all()],
                 place=past_event.place)
        )
    )

    if not is_created:
        old_event.dates.extend(old_dates if old_dates else past_event.dates)
        old_event.save()


def update_event(ev, event, json_events, place):
    """Обновление события

        ev: объект события
        event: конкретное событие из json
        json_events: все событя для места из json
        place: объект места
    """

    slug_list = [j_event["slug"] for j_event in json_events]  # список слагов тех событий, которые пришли в json

    for place_event in place.events_set.all():
        if place_event.slug not in slug_list:
            add_to_history(place_event)
            place_event.delete()

    old_dates = []
    now = int(time.time())
    for date in ev.dates:
        if date["end"] < now:
            old_dates.append(date)

    if old_dates:
        add_to_history(ev, old_dates)
        ev.dates = get_actual_dates(event["dates"])
        ev.save()
        print(f"Событие со slug: {ev.slug} обновлено")


def get_events(place, place_id):
    """Получение событий для места"""

    fields = (*common_fields, "dates", "age_restriction", "price", "tags")
    url = base_url + "events/"

    params = {
        **common_params,
        "fields": ",".join(map(str, fields)),
        "place_id": place_id,
        "actual_since": int(time.time()),
        "page_size": 100
    }

    events = get_json(url, params)

    if not events:
        return

    for event in events:
        e, is_created = Events.objects.get_or_create(
            slug=event["slug"],
            defaults=dict(
                title=event["title"],
                slug=event["slug"],
                description=event["description"],
                body_text=event["body_text"],
                age_restriction=event["age_restriction"],
                photo=[img["image"] for img in event["images"]],
                price=event["price"],
                place=place,
                dates=get_actual_dates(event["dates"])
            )
        )

        if is_created:
            get_tags(e, event["tags"])

        else:
            update_event(e, event, events, place)


def write_to_db(url, params, category):
    """Запись данных в бд"""

    global created
    data = get_json(url, params)

    for item in data:

        if item["slug"] == "teatr-na-yugo-zapade":
            continue

        place, is_created = Place.objects.get_or_create(
            slug=item["slug"],
            defaults=dict(
                title=item["title"],
                slug=item["slug"],
                description=item["description"],
                body_text=item["body_text"],
                address=item["address"],
                schedule=item["timetable"],
                phone=item["phone"],
                site=item["foreign_url"],
                photo=[img["image"] for img in item["images"]],
                category=get_category(category),
                coordinates={"lat": item["coords"]["lat"], "lon": item["coords"]["lon"]}
            )
        )

        if is_created:
            get_metro_station(place, item["subway"])
            get_tags(place, item["tags"])
            get_events(place, item["id"])

            print(f"Место со slug: {place.slug} добавлено")
            created += 1

        else:
            get_events(place, item["id"])
