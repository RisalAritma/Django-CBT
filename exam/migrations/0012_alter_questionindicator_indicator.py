# Generated by Django 4.2 on 2025-05-26 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0011_profile_jurusan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionindicator',
            name='indicator',
            field=models.TextField(),
        ),
    ]
