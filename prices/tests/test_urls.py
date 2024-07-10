from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from prices.models import Price
import datetime

User = get_user_model()

class PricesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.prices_url = reverse('Prices:price')
        self.price1 = Price.objects.create(name='Basic', value=1000, days=30)
        self.price2 = Price.objects.create(name='Premium', value=2000, days=60)

    def test_get_prices(self):
        response = self.client.get(self.prices_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prices/price.html')
        self.assertContains(response, self.price1.name)
        self.assertContains(response, self.price2.name)
