# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bid(models.Model):
    trip = models.ForeignKey('Trip', models.DO_NOTHING)
    location = models.ForeignKey('Locations', models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bid'


class Cities(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    country = models.CharField(max_length=100)
    img_url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Hotels(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotels'


class Locations(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    site_url = models.CharField(max_length=500, blank=True, null=True)
    four_square_id = models.CharField(max_length=500)
    visit_time = models.IntegerField(blank=True, null=True)
    schedule = models.CharField(max_length=1000, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    img_url = models.CharField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    price_level = models.IntegerField(blank=True, null=True)
    types = models.CharField(max_length=500, blank=True, null=True)
    user_study = models.NullBooleanField()

    def stars(self):
        return int(round(self.rating / 2))

    class Meta:
        managed = False
        db_table = 'locations'


class ScheduleDetails(models.Model):
    schedule = models.ForeignKey('Schedules', models.DO_NOTHING, blank=True, null=True)
    activity = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    activity_order = models.IntegerField(blank=True, null=True)
    activity_name = models.CharField(max_length=200, blank=True, null=True)
    activity_starts = models.CharField(max_length=50, blank=True, null=True)
    activity_ends = models.CharField(max_length=50, blank=True, null=True)
    activity_lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    activity_lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        ordering = ['activity_order']
        managed = False
        db_table = 'schedule_details'


class Schedules(models.Model):
    trip = models.ForeignKey('Trip', models.DO_NOTHING, blank=True, null=True)
    day = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['day']
        managed = False
        db_table = 'schedules'


class SelectedActivities(models.Model):
    trip = models.ForeignKey('Trip', models.DO_NOTHING)
    location = models.ForeignKey(Locations, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'selected_activities'


class Trip(models.Model):
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    owner = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField()
    bidding_ends = models.DateTimeField(blank=True, null=True)
    hotel = models.ForeignKey(Hotels, models.DO_NOTHING, blank=True, null=True)
    stage = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['created_at']
        managed = False
        db_table = 'trip'


class UsersTrip(models.Model):
    trip = models.ForeignKey(Trip, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    is_owner = models.BooleanField()
    stage = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_trip'
