# Generated by Django 2.2.2 on 2020-07-05 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200705_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]