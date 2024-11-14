# Generated by Django 3.2.3 on 2022-03-02 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0018_auto_20220302_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerAddresses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(help_text='Delivery Address', max_length=1024, null=True)),
                ('default', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(help_text='The Customer that created this delivery address', null=True, on_delete=django.db.models.deletion.CASCADE, to='amplifiedbeautyaus.customer')),
            ],
        ),
    ]