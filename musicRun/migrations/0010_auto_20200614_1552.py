# Generated by Django 3.0.7 on 2020-06-14 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicRun', '0009_auto_20200607_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifyuser',
            name='songs',
            field=models.ManyToManyField(blank=True, to='musicRun.Song'),
        ),
    ]
