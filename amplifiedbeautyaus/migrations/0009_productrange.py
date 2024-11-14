# Generated by Django 3.2.3 on 2021-12-13 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0008_customer_wishlisted_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of this Product Range', max_length=64, null=True)),
                ('image', models.ImageField(help_text='The Image for this Product Range', null=True, upload_to='product_ranges/')),
                ('products', models.ManyToManyField(to='amplifiedbeautyaus.Product')),
            ],
        ),
    ]