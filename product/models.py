from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from django_countries.fields import CountryField
from sorl.thumbnail import ImageField

from uuid import uuid4


def fill_slug_field(instance=None)-> None:
    """Helper function to fill 'slug' field after 'name' field"""
    if not instance.slug or instance._name != instance.name:
        instance.slug = slugify(instance.name)


class Category(models.Model):
    """Every Device and Product has at least one Category"""
    sub = models.ForeignKey('self',
                            verbose_name=_('sub category'),
                            on_delete=models.CASCADE,
                            related_name='category_sub',
                            blank=True,
                            null=True)
    name = models.CharField(verbose_name=_('name'), max_length=100, unique=True)
    slug = models.SlugField(blank=True)
    # _name field used to check if slug field should be changed or not
    _name = None

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Category'
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._name = self.name

    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        fill_slug_field(self)
        return super().save()
    


class Brand(models.Model):
    """Every Product has on Brand but it possible that some products does not have any"""
    name = models.CharField(verbose_name=_('name'), max_length=100, unique=True)
    country = CountryField(verbose_name=_('country'), blank=True)
    slug = models.SlugField(blank=True)
    _name = None

    class Meta:
        ordering = ('name',)
        verbose_name = 'Brand'
        verbose_name_plural = 'Brand'
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._name = self.name
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        fill_slug_field(self)
        return super().save()


class Product(models.Model):
    """Any product and accessory in the shop is an object of this model."""
    product_id = models.UUIDField(verbose_name=_('product id'), default=uuid4, blank=True, editable=False, unique=True)
    category = models.ManyToManyField('Category',
                                      verbose_name=_('category'),
                                      related_name='product_category',
                                      blank=True)
    sub = models.ForeignKey('self',
                            on_delete=models.SET_NULL,
                            verbose_name=_('parent product'),
                            related_name='sub_products',
                            blank=True,
                            null=True)
    brand = models.ForeignKey('Brand',
                              verbose_name=_('brand'),
                              related_name='product_brand',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    name = models.CharField(verbose_name=_('name'), max_length=100, unique=True)
    price = models.DecimalField(verbose_name=_('price'), max_digits=10, decimal_places=0)
    discount = models.DecimalField(verbose_name=_('discount'), max_digits=9, decimal_places=0, default=0)
    # 'describe' and 'review' will be replaced by ckeditor field
    describe = models.TextField(verbose_name=_('describe'), blank=True)
    review = models.TextField(verbose_name=_('review'), blank=True)
    # Customized 'upload to' will be added to 'background'
    main_image = ImageField(verbose_name=_('main image'), blank=True)
    background = ImageField(verbose_name=_('background image'), blank=True)
    # ContentType 'images' will be added
    color = models.ManyToManyField('Color',
                                   verbose_name=_('color'),
                                   related_name='product_color',
                                   blank=True)
    # In production we set 'stock' as a mandatory field
    stock = models.PositiveIntegerField(verbose_name=_('stock'), default=5)
    # 'is_available' changed by 'stock' value automatically
    is_available = models.BooleanField(verbose_name=_('is available'), default=True)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    _name = None

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Product'
        verbose_name_plural = 'Product'
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._name = self.name
    
    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        fill_slug_field(self)
        return super().save()
    
    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})
    
    @property
    def price_end(self):
        return int(self.price) - int(self.discount)
    

class Color(models.Model):
    """Some products have diffrent color"""
    name = models.CharField(verbose_name=_('name'), max_length=10, unique=True)
    image = ImageField(verbose_name=_('image'), blank=True)
    product = models.ManyToManyField('Product',
                                     verbose_name=_('product'),
                                     related_name='color_product',
                                     blank=True)
    slug = models.SlugField(blank=True)
    _name = None

    class Meta:
        ordering = ['name']
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._name = self.name

    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        fill_slug_field(self)
        return super().save()


class ColorPrice(models.Model):
    """For some products, each color has its own price. Some colors have diffrent prices than others"""
    product = models.ForeignKey('Product',
                                verbose_name=_('product'),
                                related_name='colorprice_product',
                                on_delete=models.CASCADE)
    color = models.ForeignKey('Color',
                              verbose_name=_('color'),
                              related_name='colorprice_color',
                              on_delete=models.CASCADE)
    extra_price = models.DecimalField(verbose_name=_('price'), max_digits=9, decimal_places=0, default=0)
    cp_stock = models.PositiveIntegerField(verbose_name=_('cp_stock'), blank=True)
    is_available = models.BooleanField(verbose_name=_('is_available'), default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
        verbose_name = 'Color Price'
        verbose_name_plural = 'Color Prices'
    
    def __str__(self):
        return f'{self.product.name}_{self.color.name}: {self.extra_price}'
    