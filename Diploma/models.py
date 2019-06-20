# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Group(models.Model):
    id_group = models.AutoField(primary_key=True)
    number = models.CharField(unique=True, max_length=4)
    teacher = models.ForeignKey('User', models.DO_NOTHING, db_column='teacher', related_name='teacher')

    def __str__(self):
        return self.number

    class Meta:
        managed = False
        db_table = 'group'


class Material(models.Model):
    id_material = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=45)
    path = models.CharField(max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'material'


class Practice(models.Model):
    id_practice = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    path = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'practice'


class PracticeForGroup(models.Model):
    id_practice = models.OneToOneField(Practice, models.DO_NOTHING,primary_key=True, db_column='id_practice', unique=True)
    id_group = models.ForeignKey(Group, models.DO_NOTHING, db_column='id_group')
    date_of_sub = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'practice_for_group'


class Theme(models.Model):
    id_theme = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    path = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'theme'


class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=45)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=45)
    sername = models.CharField(max_length=45)
    patronymic = models.CharField(max_length=45, blank=True, null=True)
    status = models.CharField(max_length=7)
    group = models.ForeignKey(Group, models.DO_NOTHING, db_column='group', blank=True, null=True)
    variant = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        user = self.sername + ' ' + self.name + ' ' + self.patronymic
        if self.group is not None:
            user = user + ' (Y' + self.group.number + ')'
        return  user

    class Meta:
        managed = False
        db_table = 'user'
