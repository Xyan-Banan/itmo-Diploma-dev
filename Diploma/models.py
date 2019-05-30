# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Groups(models.Model):
    id_group = models.AutoField(primary_key=True)
    number = models.CharField(max_length=4)
    teacher = models.ForeignKey('Users', models.DO_NOTHING, db_column='teacher')

    class Meta:
        managed = True
        db_table = 'groups'


class Practics(models.Model):
    id_practice = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'practics'


class PracticsForGroups(models.Model):
    id_practic = models.OneToOneField(Practics, models.CASCADE, db_column='id_practic')
    id_group = models.ForeignKey(Groups, models.DO_NOTHING, db_column='id_group')

    class Meta:
        managed = True
        db_table = 'practics_for_groups'


class PracticsForStudents(models.Model):
    id_practic = models.ForeignKey(Practics, models.DO_NOTHING, db_column='id_practic')
    path = models.CharField(max_length=200)
    file_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'practics_for_students'


class TasksInPractics(models.Model):
    id_practice = models.ForeignKey(Practics, models.DO_NOTHING, db_column='id_practice')
    id_theme = models.ForeignKey('Themes', models.DO_NOTHING, db_column='id_theme')
    variant = models.CharField(max_length=2)
    file_name = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'tasks_in_practics'


class Themes(models.Model):
    id_theme = models.AutoField(primary_key=True)
    theme_name = models.CharField(unique=True, max_length=100, blank=False)
    path = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'themes'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=45)
    salt = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45)
    sername = models.CharField(max_length=45)
    patronymic = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=7)
    group = models.ForeignKey(Groups, models.DO_NOTHING, db_column='group', blank=True, null=True)
    variant = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'users'
