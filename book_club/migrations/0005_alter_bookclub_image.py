# Generated by Django 4.2 on 2023-05-17 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_club', '0004_remove_bookclub_image_url_bookclub_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookclub',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
