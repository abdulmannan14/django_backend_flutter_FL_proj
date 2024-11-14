# Generated by Django 3.2.3 on 2022-03-05 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0020_auto_20220302_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='address',
            field=models.ForeignKey(blank=True, help_text='Delivery Address for this Order', null=True, on_delete=django.db.models.deletion.CASCADE, to='amplifiedbeautyaus.customeraddresses'),
        ),
    ]
