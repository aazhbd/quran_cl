# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-04 18:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('country', models.CharField(blank=True, max_length=250)),
                ('city', models.CharField(blank=True, max_length=250)),
                ('translation_type', models.CharField(blank=True, max_length=50)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
                ('enabled', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('english_name', models.CharField(max_length=1000)),
                ('arabic_name', models.CharField(max_length=1000)),
                ('transliteration', models.CharField(max_length=1000)),
                ('total_verses', models.IntegerField(blank=True, null=True)),
                ('enabled', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('vnum', models.IntegerField()),
                ('cnum', models.IntegerField()),
                ('ctext', models.TextField(verbose_name='Comment')),
                ('comment_type', models.CharField(choices=[('Translation', 'Translation'), ('Explanation', 'Explanation'), ('Question', 'Question'), ('Comments', 'Comments')], default='Question', max_length=100)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('enabled', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70)),
                ('iso_code', models.CharField(max_length=50)),
                ('direction', models.IntegerField()),
                ('enabled', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('number', models.IntegerField()),
                ('vtext', models.CharField(max_length=10000)),
                ('enabled', models.IntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='quran.Author')),
                ('chapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chapter', to='quran.Chapter')),
                ('vlang', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verse_language', to='quran.Language')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='alang',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_language', to='quran.Language'),
        ),
    ]
