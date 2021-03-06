# Generated by Django 4.0.4 on 2022-05-08 14:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AppStore', '0003_rename_image_app_appimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='developer',
            name='company',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='developer',
            name='company_description',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='developer',
            name='website',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
