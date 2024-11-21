# Generated by Django 4.2.16 on 2024-11-18 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_brand_alter_contactrequest_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(choices=[('OPPO', 'OPPO'), ('Xiaomi', 'Xiaomi'), ('Samsung', 'Samsung'), ('Honor', 'Honor'), ('Google', 'Google'), ('ZTE', 'ZTE'), ('Apple', 'Apple')], default='Невiдомий', max_length=250, verbose_name='Бренд'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='products/%Y/%m/%d')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
            options={
                'verbose_name': 'Зображення товару',
                'verbose_name_plural': 'Зображення товарів',
            },
        ),
    ]
