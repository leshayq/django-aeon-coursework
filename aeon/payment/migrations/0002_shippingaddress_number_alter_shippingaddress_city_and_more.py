# Generated by Django 4.2.16 on 2024-11-08 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='number',
            field=models.CharField(default=380999999999, max_length=15, verbose_name='Номер телефону'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Місто'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='department',
            field=models.IntegerField(blank=True, null=True, verbose_name='Відділення'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Електронна пошта'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='ПІБ'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Адреса'),
        ),
    ]