# Generated by Django 3.2.3 on 2022-03-23 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0033_alter_productimages_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
