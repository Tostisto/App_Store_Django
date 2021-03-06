# Generated by Django 4.0.4 on 2022-05-06 17:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AppStore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='appFile',
            field=models.FileField(default=django.utils.timezone.now, upload_to='files/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='app',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='images/'),
            preserve_default=False,
        ),
    ]
