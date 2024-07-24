from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from account.factories import UserFactory
from customer.factories import CustomerFactory, AddressFactory
from inventory.factories import InventoryFactory
from order.factories import OrderFactory, OrderItemFactory
from order.models import Order
from services.test_utils import CustomAPITestCase


class AdminOrderListCreateAPIViewTest(CustomAPITestCase):
    def setUp(self):
        self.fake = Faker()

        self.user = UserFactory()
        self.customer = CustomerFactory()
        self.address = AddressFactory(customer=self.customer)
        self.inventory = InventoryFactory(amount="1000.564", executed_amount="0", price="35.54", visible=True)
        self.order1 = OrderFactory(customer=self.customer, creator=self.user, status="0")
        self.order2 = OrderFactory(customer=self.customer, creator=self.user, status="1")
        self.order1_item1 = OrderItemFactory(
            order=self.order1, product=self.inventory, executor=self.user, creator=self.user, amount="30.358"
        )
        self.order1_item2 = OrderItemFactory(
            order=self.order1, product=self.inventory, executor=self.user, creator=self.user, amount="31.226"
        )
        self.order2_item1 = OrderItemFactory(
            order=self.order2, product=self.inventory, executor=self.user, creator=self.user, amount="32.432"
        )

        self.client = APIClient()
        self.client.force_login(user=self.user)
        self.url = reverse("order:v2:admin:order_list_create")

    def test_list_orders(self):
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 2)

        expected_response = {
            "id": self.order2.id,
            "address": self.order2.address,
            "status": "in_progress",
            "creator": self.user.id,
        }
        expected_customer_response = {
            "id": self.customer.id,
            "name": self.customer.name,
            "phone_number": self.customer.phone_number,
            "additional_data": self.customer.additional_data,
            "addresses": [{"id": self.address.id, "address": self.address.address}],
        }
        expected_order_item_response = {
            "id": self.order2_item1.id,
            "code": self.inventory.code,
            "name": self.inventory.name,
            "price": "35.54",
            "amount": "32.432",
            "total": "1152.63328",
            "comment": None,
            "status": "pending",
            "order": self.order2.id,
            "product": self.inventory.id,
            "executor": self.user.id,
            "creator": self.user.id,
        }
        expected_product_response = {
            "id": self.inventory.id,
            "name": self.inventory.name,
            "code": self.inventory.code,
            "visible": True,
            "price": "35.54",
            "max_price": str(self.inventory.max_price),
            "unit": self.inventory.unit,
            "comment": None,
            "image_url": None,
            "description": None,
            "store": self.inventory.store.name,
            "category": self.inventory.category.path,
        }
        self.assertDictIncludes(response.data[0], expected_response)
        self.assertDictIncludes(response.data[0]["customer"], expected_customer_response)
        self.assertDictIncludes(response.data[0]["order_items"][0], expected_order_item_response)
        self.assertDictIncludes(response.data[0]["order_items"][0]["product_info"], expected_product_response)
