import random
import string
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from users.models import CustomUser

User = get_user_model()

def rand_slug():
    """
    Generate a random slug consisting of letters and digits.

    Returns:
        str: The randomly generated slug.

    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))

class Category(models.Model):
    name = models.CharField('Категорія', max_length=250, db_index=True)
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    icon = models.ImageField('Іконка', null=True, blank=True, upload_to='icons/')

    class Meta:
        unique_together = (['slug'])
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("shop:category_list", args=[str(self.slug)])
    
class Brand(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренди'

    def __str__(self):
        return self.name

class Product(models.Model):
    BRAND_CHOICES = [(i, i) for i in Brand.objects.values_list('name', flat=True)]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Назва', max_length=250)
    brand = models.CharField('Бренд', max_length=250, default='Невiдомий', choices=BRAND_CHOICES)
    color = ColorField(default='#FF0000', null=False, blank=True)
    description = models.TextField('Опис', blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Ціна', max_digits=10, decimal_places=2, default=99.99)
    image = models.ImageField('Зображення', upload_to='products/%Y/%m/%d')
    available = models.BooleanField('Наявність', default=True)
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    updated_at = models.DateTimeField('Дата оновлення', auto_now=True)

        
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def average_rating(self) -> float:
        return Rating.objects.filter(product=self).aggregate(Avg("rating"))["rating__avg"] or 0


    def save(self, *args, **kwargs):
        self.__class__.BRAND_CHOICES = [(i, i) for i in Brand.objects.values_list('name', flat=True)]
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={'slug': self.slug, 'category__slug': self.category.slug})
    
class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(ProductManager, self).get_queryset().filter(available=True)     
       
class ProductProxy(Product):
    
    objects = ProductManager()
    class Meta:
        proxy = True

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Оцінка'
        verbose_name_plural = 'Оцінки'
        
    def __str__(self):
        return f"{self.product.title}: {self.rating}"
    
class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductProxy, blank=True)

    def get_total_products(self):
        return self.products.count()
    
class ImageSlider(models.Model):
    product = models.ForeignKey(ProductProxy, on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдери'

class ContactRequest(models.Model):
    SUBJECT_CHOICES = [
    ('Замовлення', 'Замовлення'),
    ('Скарга', 'Скарга'),
    ('Пропозиція', 'Пропозиція'),
    ('Помилка', 'Помилка'),
    ('Інше', 'Інше')
    ]
    name = models.CharField("Ім'я", max_length=100)
    contact_info = models.CharField('Телефон/e-mail', max_length=255)
    subject = models.CharField('Тема', max_length=100, choices=SUBJECT_CHOICES)
    message = models.TextField('Повідомлення')
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Звернення'
        verbose_name_plural = 'Звернення'

    def __str__(self):
        return f"Запит від {self.name} - {self.subject}"