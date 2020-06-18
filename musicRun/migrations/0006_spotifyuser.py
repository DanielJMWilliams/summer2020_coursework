# Generated by Django 3.0.6 on 2020-06-07 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicRun', '0005_auto_20200604_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpotifyUser',
            fields=[
                ('spotify_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('songs', models.ManyToManyField(blank=True, to='musicRun.Song')),
            ],
        ),
    ]