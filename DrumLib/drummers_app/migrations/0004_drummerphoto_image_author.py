# Generated by Django 4.2.6 on 2024-06-05 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drummers_app', '0003_alter_drummerphoto_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='drummerphoto',
            name='image_author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
