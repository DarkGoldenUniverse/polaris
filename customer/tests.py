from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from customer.models import Customer
from services.test_utils import CustomAPITestCase


class CustomerApiTests(CustomAPITestCase):
    def setUp(self):
        self.fake = Faker()
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")

        self.client = APIClient()
        self.client.login(username="testuser", password="testpass")

        self.customer1 = Customer.objects.create(
            name=self.fake.name(), phone_number=self.fake.random_int(1000000000, 8999999999999)
        )
        self.customer2 = Customer.objects.create(
            name=self.fake.name(), phone_number=self.fake.random_int(1000000000, 8999999999999)
        )

    def test_list_customers(self):
        customer = Customer.objects.create(name="Customer FullName", phone_number="9999999999999")

        url = reverse("customer:v2:admin:customer_list_create")
        response = self.client.get(url)

        expected_response = {
            "id": customer.id,
            "name": "Customer FullName",
            "phone_number": "9999999999999",
            "additional_data": {},
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertDictIncludes(response.data[0], expected_response)

    def test_create_customer(self):
        url = reverse("customer:v2:admin:customer_list_create")
        data = {"name": self.fake.name(), "phone_number": self.fake.random_int(1000000000, 8999999999999)}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(Customer.objects.get(phone_number=data["phone_number"]).name, data["name"])

    def test_duplicate_create_customer(self):
        Customer.objects.create(name="Customer FullName", phone_number="9999999999999")

        url = reverse("customer:v2:admin:customer_list_create")
        data = {"name": self.fake.name(), "phone_number": "9999999999999"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(response.data["phone_number"][0], "customer with this phone number already exists.")

    def test_retrieve_customer(self):
        url = reverse("customer:v2:admin:customer_detail", kwargs={"pk": self.customer1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone_number"], self.customer1.phone_number)

    def test_retrieve_customer_not_found(self):
        url = reverse("customer:v2:admin:customer_detail", kwargs={"pk": 0})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_customer_action(self):
    #     url = reverse('customer_action', kwargs={'pk': self.customer1.pk})
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['status'], 'action performed')
    #
    # def test_customer_action_not_found(self):
    #     url = reverse('customer_action', kwargs={'pk': 999})
    #     response = self.client.post(url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
