from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Sale
from datetime import date

class SimpleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u', password='p')

    def test_login_required(self):
        resp = self.client.get(reverse('dashboard:index'))
        self.assertEqual(resp.status_code, 302)

    def test_create_sale(self):
        self.client.login(username='u', password='p')
        Sale.objects.create(date=date.today(), product='Produto', category='Categoria', unit_price=10, quantity=2)
        resp = self.client.get(reverse('dashboard:sale_list'))
        self.assertEqual(resp.status_code, 200)
