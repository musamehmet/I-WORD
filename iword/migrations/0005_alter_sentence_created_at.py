# Generated by Django 4.2.6 on 2023-10-17 17:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('iword', '0004_sentence_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]