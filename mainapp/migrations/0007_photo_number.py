# Generated by Django 2.1.5 on 2019-08-06 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20190315_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='number',
            field=models.SmallIntegerField(default=0, verbose_name='Порядок вывода'),
        ),
    ]
