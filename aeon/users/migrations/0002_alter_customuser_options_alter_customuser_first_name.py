# Generated by Django 4.2.16 on 2024-11-16 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Користувач', 'verbose_name_plural': 'Користувачі'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name="Ім'я"),
        ),
    ]