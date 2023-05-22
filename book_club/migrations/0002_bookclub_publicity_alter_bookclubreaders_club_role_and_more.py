# Generated by Django 4.2 on 2023-05-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_club', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookclub',
            name='publicity',
            field=models.CharField(choices=[('PB', 'Public'), ('OB', 'Observable'), ('PR', 'Private')], default='PB', max_length=2),
        ),
        migrations.AlterField(
            model_name='bookclubreaders',
            name='club_role',
            field=models.CharField(choices=[('AD', 'Admin'), ('PT', 'Participant'), ('RD', 'Reader'), ('OB', 'Observer')], default='RD', max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='bookclubreaders',
            unique_together={('reader', 'book_club')},
        ),
    ]