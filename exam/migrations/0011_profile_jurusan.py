# Generated by Django 4.2 on 2025-05-26 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0010_alter_questionanswer_random'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='jurusan',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
