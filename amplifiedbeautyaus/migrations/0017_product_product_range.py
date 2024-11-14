# Generated by Django 3.2.3 on 2022-03-02 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0016_auto_20220302_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_range',
            field=models.ForeignKey(blank=True, default='1', help_text='Product Range for this Product', null=True, on_delete=django.db.models.deletion.CASCADE, to='amplifiedbeautyaus.productrange'),
        ),
    ]
