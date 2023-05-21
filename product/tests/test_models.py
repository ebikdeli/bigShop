from django.test import TestCase
from django_countries.fields import Country

from product.models import Category, Brand, Device,\
                        Product, Color, ColorPrice


class TestCategory(TestCase):
    """Category test methods"""
    def test_category_create(self):
        """Test if category created successfully"""
        category = Category.objects.create(name='laptop')
        self.assertIsNotNone(category)

    def test_category_update(self):
        """Test if category updated properly"""
        category = Category.objects.create(name='laptop')
        self.assertNotEqual(category.name, 'phone')

        category.name = 'phone'
        category.save()
        self.assertEqual(category.name, 'phone')

    def test_category_delete(self):
        """Test if category deleted successfully"""
        category = Category.objects.create(name='laptop')
        self.assertIn(category, Category.objects.all())

        Category.objects.filter(name=category.name).delete()
        self.assertNotIn(category, Category.objects.all())
    
    def test_category_inner_create(self):
        """Test if inner categories could be created"""
        category_electronic = Category.objects.create(name='electronic')
        category_laptop = Category.objects.create(sub=category_electronic, name='laptop')
        self.assertEqual(category_laptop.sub, category_electronic)
        self.assertIn(category_laptop, category_electronic.category_sub.all())
    
    def test_category_inner_update_delete(self):
        """Test if inner categories could be updated and deleted successfully"""
        category_electronic = Category.objects.create(name='electronic')
        category_inner = Category.objects.create(sub=category_electronic, name='laptop')
        self.assertEqual(category_inner.name, 'laptop')

        # Updated 'name' of inner category
        category_inner.name = 'iphone'
        category_inner.save()
        self.assertEqual(category_inner.name, 'iphone')
        self.assertIn(category_inner, category_electronic.category_sub.all())

        # Delete inner category
        category_inner.delete()
        self.assertNotIn(category_inner, category_electronic.category_sub.all())
    
    def test_category_slug_field_change(self):
        """Check if category slug field changed correctly"""
        category = Category.objects.create(name='laptop')
        laptop_slug = category.slug
        category.name = 'iphone 14'
        category.save()
        iphone_slug = category.slug
        self.assertNotEqual(laptop_slug, iphone_slug)


class TestBrand(TestCase):
    """Test Brand"""
    def test_brand_create(self):
        """Test if brand created successfully"""
        brand = Brand.objects.create(name='Apple', country='USA')
        self.assertEqual(brand.name, 'Apple')
    
    def test_brand_update(self):
        """Test if brand updated successfully"""
        brand = Brand.objects.create(name='Apple')
        self.assertEqual(brand.name, 'Apple')

        brand.name = 'Samsung'
        self.assertNotEqual(brand.name, 'Apple')
    
    def test_brand_delete(self):
        """Test if brand deleted properly"""
        brand = Brand.objects.create(name='Apple')
        self.assertIn(brand, Brand.objects.all())

        brand.delete()
        self.assertNotIn(brand, Brand.objects.all())
    
    def test_brand_country_field_create(self):
        """Test country field of the brand"""
        brand = Brand.objects.create(name='Apple', country='US')
        self.assertEqual(brand.country, Country(code='US'))
    
    def test_brand_country_field_update(self):
        """Test if country field updated"""
        brand = Brand.objects.create(name='Apple', country='US')
        brand.country = 'UK'
        brand.save()
        self.assertEqual(brand.country, Country(code='UK'))
    
    def test_brand_country_field_delete(self):
        """Test if country field deleted"""
        brand = Brand.objects.create(name='Apple', country='US')
        self.assertEqual(brand.country, Country(code='US'))

        brand.country = ''
        brand.save()
        self.assertEqual(brand.country, str())
    
    def test_brand_slug_field_change(self):
        """Check if brand slug field changed correctly"""
        brand = Brand.objects.create(name='Apple')
        appleSlug = brand.slug
        brand.name = 'Samsung'
        brand.save()
        samsungSlug = brand.slug
        self.assertNotEqual(appleSlug, samsungSlug)


class TestDevice(TestCase):
    """Device test methods"""
    def setUp(self) -> None:
        self.category_electronic = Category.objects.create(name='electronic')
        self.category_phone = Category.objects.create(sub=self.category_electronic, name='phone')
        self.brand = Brand.objects.create(name='Apple', country='US')
    
    def test_device_create(self):
        """Test if device created successfully"""
        device = Device.objects.create(name='Iphone 14 Pro max')
        self.assertEqual(device.name, 'Iphone 14 Pro max')
    
    def test_device_update(self):
        """Test if device updated successfully"""
        device = Device.objects.create(name='Iphone 14 Pro max')
        self.assertEqual(device.name, 'Iphone 14 Pro max')

        device.name = 'Iphone 13'
        device.save()
        self.assertEqual(device.name, 'Iphone 13')
    
    def test_device_delete(self):
        """Test if device deleted"""
        device = Device.objects.create(name='Iphone 14 Pro max')
        self.assertIn(device, Device.objects.all())

        Device.objects.filter(name='Iphone 14 Pro max').delete()
        self.assertNotIn(device, Device.objects.all())
    
    def test_device_category(self):
        """Test if category added to device properly"""
        # Create device object
        device = Device.objects.create(name='Iphone 14 Pro max')
        self.assertEqual(device.name, 'Iphone 14 Pro max')
        self.assertNotIn(self.category_electronic, device.category.all())

        # 'category_electronic' must not have any relation with devices
        self.assertNotIn(device, self.category_electronic.device_category.all())

        # Add 'category_electronic' to device.category
        device.category.add(self.category_electronic)
        self.assertIn(self.category_electronic, device.category.all())

        # 'category_electronic' must have device as relation
        self.assertIn(device, self.category_electronic.device_category.all())
    
    def test_device_inner_category(self):
        """Test if inner category has chained relationship with device"""
        device = Device.objects.create(name='Iphone 14 Pro max')
        self.assertEqual(device.name, 'Iphone 14 Pro max')
        self.assertNotIn(self.category_phone, device.category.all())

        # 'category_phone' must not have any relation with devices
        self.assertNotIn(device, self.category_phone.device_category.all())

        # Add 'category_phone' parent to device.category
        device.category.add(self.category_phone)
        self.assertIn(self.category_phone, device.category.all())
        self.assertNotIn(self.category_electronic, device.category.all())

        # Add 'category_phone' parent to device.category
        device.category.add(self.category_phone.sub)
        self.assertIn(self.category_electronic, device.category.all())
    
    def test_device_slug_field_change(self):
        """Check if device slug field changed correctly"""
        device = Device.objects.create(name='Imac')
        imacSlug = device.slug
        device.name = 'Iphone'
        device.save()
        IphoneSlug = device.slug
        self.assertNotEqual(imacSlug, IphoneSlug)


class TestProduct(TestCase):
    """Product test methods"""
    def setUp(self) -> None:
        self.category = Category.objects.create(name='laptop')
        self.brand = Brand.objects.create(name='Apple')
        device_data = {'name': 'Laptop', 'year': '2022'}
        self.device = Device.objects.create(**device_data)
        self.device.category.add(self.category)
        self.color = Color.objects.create(name='red')

    def test_product_create(self):
        """Test if product created properly"""
        product_data = {
            'brand': self.brand,
            'name': 'iphone 14 pro max',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        self.assertEqual(product.stock, 6)
    
    def test_product_update(self):
        """Test if product updated properly"""
        product_data = {
            'brand': self.brand,
            'name': 'iphone 14 pro max',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        product.stock = 12
        product.save()
        self.assertNotEqual(product.stock, 6)
    
    def test_product_delete(self):
        """Test if product deleted properly"""
        product_data = {
            'brand': self.brand,
            'name': 'iphone 14 pro max',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        self.assertIn(product, Product.objects.all())

        product.delete()
        self.assertNotIn(product, Product.objects.all())
    
    def test_product_add_category(self):
        """Test if category could be added"""
        product_data = {
            'brand': self.brand,
            'name': 'iphone 14 pro max',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        self.assertNotIn(self.category, product.category.all())

        product.category.add(self.category)
        self.assertIn(self.category, product.category.all())

        product.category.remove(self.category)
        self.assertNotIn(self.category, product.category.all())
    
    def test_product_add_device_category_color(self):
        """Test if adding many objects to product does not return any error"""
        product_data = {
            'brand': self.brand,
            'name': 'iphone 14 pro max',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        self.assertNotIn(self.category, product.category.all())
        self.assertNotIn(self.device, product.device.all())
        self.assertNotIn(self.color, product.color.all())

        # Add the objects to the product
        product.category.add(self.category)
        product.device.add(self.device)
        product.color.add(self.color)
        self.assertIn(self.category, product.category.all())
        self.assertIn(self.device, product.device.all())
        self.assertIn(self.color, product.color.all())
    
    def test_product_slug_field_change(self):
        """Check if product slug field changed correctly"""
        product_data = {
            'brand': self.brand,
            'name': 'apple watch pro',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        appleWatchSlug = product.slug
        product.name = 'Iphone 13 pro max'
        product.save()
        IphoneSlug = product.slug
        self.assertNotEqual(appleWatchSlug, IphoneSlug)
    
    def test_color_slug_field_change(self):
        """Check if color slug field changed correctly"""
        color = Color.objects.create(name='brown')
        BrownSlug = color.slug
        color.name = 'blue'
        color.save()
        blueSlug = color.slug
        self.assertNotEqual(BrownSlug, blueSlug)
    
    def test_stock_is_not_available(self):
        """Test if 'stock' is empty, turn 'is_available' to False"""
        product_data = {
            'brand': self.brand,
            'name': 'apple watch pro',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        product = Product.objects.create(**product_data)
        self.assertTrue(product.is_available)

        product.stock = 0
        product.save()
        self.assertFalse(product.is_available)

        product.stock += 1
        product.save()
        self.assertTrue(product.is_available)
    
    def test_stock_is_available(self):
        """Test if 'stock' is 'not' empty, turn 'is_available' to True"""
        product_data = {
            'brand': self.brand,
            'name': 'apple watch pro',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 0,
            'is_available': True    # It has no effect because in signal, 'is_available' turned to 'False' by 'stock = 0'
        }
        product = Product.objects.create(**product_data)
        self.assertFalse(product.is_available)

        product.stock = 10
        product.save()
        self.assertTrue(product.is_available)


class TestColorPrice(TestCase):
    """ColorPrice test methods"""
    def setUp(self) -> None:
        product_data = {
            'name': 'iphone 14 pro max',
            'price': 5000000,
            'describe': 'This is a beautiful phone',
            'review': 'Good review',
            'stock': 6,
            'is_available': True
        }
        self.product = Product.objects.create(**product_data)
        self.color = Color.objects.create(name='red')
    
    def test_colorprice_create(self):
        """Test if ColorPrice created successfully"""
        color_price = ColorPrice.objects.create(
            product=self.product,
            color=self.color,
            extra_price=6500
        )
        self.assertEqual(color_price.extra_price, 6500)
    
    def test_colorprice_update(self):
        """Test if ColorPrice updated successfully"""
        color_price = ColorPrice.objects.create(
            product=self.product,
            color=self.color,
            extra_price=6500
        )
        self.assertEqual(color_price.extra_price, 6500)

        color_price.extra_price += 1000
        color_price.save()
        self.assertEqual(color_price.extra_price, 7500)
    
    def test_colorprice_delete(self):
        """Test if ColorPrice deleted properly"""
        color_price = ColorPrice.objects.create(
            product=self.product,
            color=self.color,
            extra_price=6500
        )
        self.assertIn(color_price, ColorPrice.objects.all())

        color_price.delete()
        self.assertNotIn(color_price, ColorPrice.objects.all())
