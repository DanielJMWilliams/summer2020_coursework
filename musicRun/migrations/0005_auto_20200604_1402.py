# Generated by Django 3.0.6 on 2020-06-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicRun', '0004_auto_20200604_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='artists',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='song',
            name='bpm',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='song',
            name='danceability',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='song',
            name='energy',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='song',
            name='valence',
            field=models.FloatField(),
        ),
    ]