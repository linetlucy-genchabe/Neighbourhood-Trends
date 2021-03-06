# Generated by Django 3.0 on 2022-06-18 13:02

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Neighbourhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('occupants_count', models.IntegerField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('country', django_countries.fields.CountryField(default='NG', max_length=2)),
                ('Admin', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'My Neighbourhood',
                'verbose_name_plural': 'Neighbourhoods',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('photo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('neighbourhood', models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='trends.Neighbourhood')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('author_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trends.Profile')),
                ('neighbourhood', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trends.Neighbourhood')),
            ],
            options={
                'verbose_name': 'My Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('address', models.TextField()),
                ('Admin', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('admin_profile', models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='trends.Profile')),
                ('neighbourhood', models.ForeignKey(blank=True, default='1', on_delete=django.db.models.deletion.CASCADE, to='trends.Neighbourhood')),
            ],
            options={
                'verbose_name': 'My Business',
                'verbose_name_plural': 'Business',
                'ordering': ['-pub_date'],
            },
        ),
    ]
