from django.db import migrations, models
import django.db.models.deletion

def migrate_brand_data(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Brand = apps.get_model('shop', 'Brand')

    for product in Product.objects.all():
        brand, _ = Brand.objects.get_or_create(name=product.brand)
        product.brand_id = brand.id
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_productimage_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_fk',
            field=models.ForeignKey(
                to='shop.Brand',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
            ),
        ),
        migrations.RunPython(migrate_brand_data),
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='brand_fk',
            new_name='brand',
        ),
    ]
