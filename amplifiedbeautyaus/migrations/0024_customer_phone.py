# Generated by Django 3.2.3 on 2022-03-06 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0023_passwordresetcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(help_text='Customers Phone Number', max_length=12, null=True),
        ),
    ]