# Generated by Django 3.2.12 on 2022-02-10 23:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_profile_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='color',
        ),
    ]