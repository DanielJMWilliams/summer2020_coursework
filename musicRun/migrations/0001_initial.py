# Generated by Django 3.0.6 on 2020-05-28 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('artist', models.CharField(max_length=64)),
                ('spotify_uri', models.CharField(max_length=64)),
                ('bpm', models.IntegerField()),
            ],
        ),
    ]
