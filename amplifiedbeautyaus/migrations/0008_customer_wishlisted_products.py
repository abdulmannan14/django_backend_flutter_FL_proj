# Generated by Django 3.2.3 on 2021-11-22 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0007_useralert'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='wishlisted_products',
            field=models.ManyToManyField(to='amplifiedbeautyaus.Product'),
        ),
    ]