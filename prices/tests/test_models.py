from django.test import TestCase
from django.urls import reverse
from prices.models import Price

class PriceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Price.objects.create(name='Basic', days=30, value=1000)
        Price.objects.create(name='Premium', days=60, value=2000)

    def test_name_label(self):
        price = Price.objects.get(id=1)
        field_label = price._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'عنوان')

    def test_days_label(self):
        price = Price.objects.get(id=1)
        field_label = price._meta.get_field('days').verbose_name
        self.assertEqual(field_label, 'روز های اشتراک')

    def test_value_label(self):
        price = Price.objects.get(id=1)
        field_label = price._meta.get_field('value').verbose_name
        self.assertEqual(field_label, 'قیمت')

    def test_ordering(self):
        prices = Price.objects.all()
        self.assertEqual(list(prices.values_list('id', flat=True)), [1, 2])  # Ensure ordering by 'days'

    def test_str_method(self):
        price = Price.objects.get(id=1)
        self.assertEqual(str(price), 'Basic')  # Adjust based on your __str__ method implementation
