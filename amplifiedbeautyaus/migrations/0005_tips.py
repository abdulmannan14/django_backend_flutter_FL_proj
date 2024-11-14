# Generated by Django 3.2.3 on 2021-11-22 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amplifiedbeautyaus', '0004_alter_productreviews_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tips',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name for this Tip', max_length=64, null=True)),
                ('image', models.ImageField(help_text='The Image for this Tip', null=True, upload_to='tips/')),
                ('content', models.TextField(help_text='The Text to show inside this Tip', max_length=1024, null=True)),
            ],
        ),
    ]