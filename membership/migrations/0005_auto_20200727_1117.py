# Generated by Django 2.2.2 on 2020-07-27 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0004_auto_20200727_1111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membershiptype',
            old_name='stripe_monthly_product_id',
            new_name='stripe_monthly_price_id',
        ),
        migrations.RenameField(
            model_name='membershiptype',
            old_name='stripe_yearly_product_id',
            new_name='stripe_yearly_price_id',
        ),
    ]
