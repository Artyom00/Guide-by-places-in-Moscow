from django.core.management.base import BaseCommand
from . import _private


class Command(BaseCommand):
    help = "Загрузка данных в бд"

    def handle(self, *args, **options):
        url = _private.base_url + "places/"
        fields = (*_private.common_fields, "id", "address", "timetable", "phone", "subway", "foreign_url", "coords", "tags")
        categories = ("theatre", "park", "palace", "museums", "cinema", "attractions", "amusement")

        for category in categories:
            params = {
                **_private.common_params,
                "categories": category,
                "fields": ",".join(map(str, fields)),
                "page_size": 50

            }

            _private.write_to_db(url, params, params["categories"])

        self.stdout.write(f"\nДобавлено новых мест: {_private.created}")
