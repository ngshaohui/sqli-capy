# Generated by Django 5.2.1 on 2025-06-04 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('rating', models.IntegerField()),
                ('image', models.CharField(max_length=256)),
                ('date', models.DateField()),
            ],
        ),
    ]
