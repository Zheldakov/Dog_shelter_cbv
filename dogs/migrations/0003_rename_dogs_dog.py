# Generated by Django 5.0.9 on 2024-10-10 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_dogs'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dogs',
            new_name='Dog',
        ),
    ]
