# Generated by Django 3.0.4 on 2020-05-23 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='', null=True, upload_to=''),
        ),
    ]
