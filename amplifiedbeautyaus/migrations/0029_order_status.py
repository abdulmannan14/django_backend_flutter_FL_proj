# Generated by Django 3.2.3 on 2022-03-06 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0028_alter_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Order Placed'), (2, 'Preparing your Order'), (3, 'Order Shipped')], default=1),
        ),
    ]
