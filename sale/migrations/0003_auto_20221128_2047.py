# Generated by Django 3.2.13 on 2022-11-28 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0002_auto_20221128_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changelog',
            name='Note',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='Note',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='Note',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
