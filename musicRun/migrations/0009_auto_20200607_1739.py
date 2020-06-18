# Generated by Django 3.0.6 on 2020-06-07 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicRun', '0008_auto_20200607_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='spotifyuser',
            name='songs',
            field=models.ManyToManyField(blank=True, to='musicRun.Song'),
        ),
    ]