# Generated by Django 3.2.16 on 2022-10-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_ad_pets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='pets',
        ),
        migrations.AddField(
            model_name='ad',
            name='pets',
            field=models.CharField(choices=[('cat', 'Cat'), ('dog', 'Dog'), ('bird', 'Bird'), ('horse', 'Horse'), ('wildanimal', 'Wild animal'), ('exoticanimal', 'Exotic animal'), ('mammal', 'Mammal'), ('fish', 'Fish'), ('reptile', 'Reptile'), ('insecs', 'Insect'), ('other', 'Other'), ('unspecified', 'Unspecified')], default='unspecified', max_length=30),
        ),
    ]
