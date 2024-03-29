# Generated by Django 5.0.2 on 2024-02-20 21:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(max_length=36)),
                ('code', models.CharField(max_length=36)),
                ('target', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'verifs',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='VerifLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('target', models.CharField(max_length=50)),
                ('ips', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=36), default=list, size=None)),
            ],
            options={
                'db_table': 'verif_logs',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='WhitelistTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(max_length=36, unique=True)),
            ],
            options={
                'db_table': 'whitelist_target',
                'ordering': ['-id'],
            },
        ),
    ]
