# Generated by Django 3.1.3 on 2020-12-17 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='category_pics'),
        ),
    ]
