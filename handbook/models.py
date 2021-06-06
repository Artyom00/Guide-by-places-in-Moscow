from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "category"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('objects_list', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('update_rubric', kwargs={'slug': self.slug})


class Place(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    schedule = models.TextField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    subway = models.ManyToManyField("Subway", blank=True, related_name="places")
    site = models.URLField(blank=True)
    photo = ArrayField(models.URLField(blank=True))
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField("Tag", related_name="places", blank=True)
    coordinates = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "place"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('place_description', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('edit_place', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_place', kwargs={'slug': self.slug})


class Subway(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = "subway"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subway_places', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('edit_station', kwargs={'slug': self.slug})


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        db_table = "tag"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag_objects', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('edit_tag', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_tag', kwargs={'slug': self.slug})


class Events(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    dates = models.JSONField(blank=True)
    age_restriction = models.CharField(max_length=3, blank=True, null=True)
    photo = ArrayField(models.URLField(blank=True))
    price = models.CharField(max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, related_name="events", blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = "events"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_description', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('edit_event', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('delete_event', kwargs={'slug': self.slug})

    def get_add_to_archive_url(self):
        return reverse('add_to_archive_url', kwargs={'slug': self.slug})


class History(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    body_text = models.TextField(blank=True)
    dates = models.JSONField(blank=True)
    age_restriction = models.CharField(max_length=3, blank=True, null=True)
    photo = ArrayField(models.URLField(blank=True))
    price = models.CharField(max_length=100, blank=True)
    tags_list = ArrayField(models.CharField(max_length=100))
    place = models.ForeignKey(Place, on_delete=models.CASCADE, blank=True)

    class Meta:
        db_table = "history"
        ordering = ["title"]

    def __str__(self):
        return self.title
