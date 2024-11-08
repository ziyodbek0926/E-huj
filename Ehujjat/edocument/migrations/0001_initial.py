# Generated by Django 5.1.2 on 2024-11-01 06:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tashkilot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomi', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=150, null=True)),
                ('zayafka_vaqti', models.DateTimeField(auto_now_add=True)),
                ('tekshirilgan_vaqti', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('tashkilot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edocument.tashkilot')),
            ],
        ),
        migrations.CreateModel(
            name='UserP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]