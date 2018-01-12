# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cities(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'cities'


class Locations(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    map_url = models.CharField(max_length=500)
    site_url = models.CharField(max_length=500, blank=True, null=True)
    google_id = models.CharField(max_length=500)
    visit_time = models.IntegerField(blank=True, null=True)
    schedule = models.CharField(max_length=1000, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'locations'


class Trip(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField()
    bidding_ends = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trip'


class Users(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'users'
