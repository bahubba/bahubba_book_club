# Generated by Django 4.2 on 2023-05-14 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_club', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='given_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='reader',
            name='surname',
            field=models.CharField(max_length=50, null=True),
        ),
    ]