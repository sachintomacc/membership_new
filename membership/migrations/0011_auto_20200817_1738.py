# Generated by Django 2.2.2 on 2020-08-17 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0010_auto_20200814_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='email',
            new_name='donor_email',
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
