import unittest
from django.urls import reverse
from django.test import Client
from .models import CustomUser

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.user = Client()
        # self.user = CustomUser.objects.create(email='mail@mail1.com',group_type='BRONZE')
        # self.user, _ = CustomUser.objects.get_or_create(email='admin@gmail.com')

    def api_response(self):
        response = self.user.get("/api/books/")
        self.assertEqual(response.status_code, 200)

    def logged_in(self):
        login_url = 'http://localhost:8000/admin/login/?next=/admin/login'
        response = self.user.post(login_url, {
            'email': 'admin@gmail.com',
            'password': 'admin',
        })
        self.assertEqual(response.status_code, 200)

    def check_bronze(self):
        response = self.user.get("/api/books/")
        self.assertEqual(response.status_code, 200)