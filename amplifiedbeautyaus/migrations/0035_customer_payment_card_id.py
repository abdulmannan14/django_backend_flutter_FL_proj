# Generated by Django 3.2.3 on 2022-04-04 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0034_remove_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='payment_card_id',
            field=models.CharField(help_text='Payment Card ID', max_length=128, null=True),
        ),
    ]
