# Generated by Django 5.1 on 2024-08-22 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='tdindex',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
