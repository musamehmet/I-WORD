# Generated by Django 4.2.6 on 2023-10-17 17:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('iword', '0003_alter_word_prontype_alter_word_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sentence',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
