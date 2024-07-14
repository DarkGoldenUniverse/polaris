import pdb

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
        self.inventory = InventoryFactory(amount=1000, executed_amount=0, visible=True)
        self.order1 = OrderFactory(customer=self.customer, creator=self.user)
        self.order2 = OrderFactory(customer=self.customer, creator=self.user)
        self.order1_item1 = OrderItemFactory(
            order=self.order1, product=self.inventory, executor=self.user, creator=self.user
        )
        self.order1_item2 = OrderItemFactory(
            order=self.order1, product=self.inventory, executor=self.user, creator=self.user
        )
        self.order2_item1 = OrderItemFactory(
            order=self.order2, product=self.inventory, executor=self.user, creator=self.user
        )

        self.client = APIClient()
        self.client.force_login(user=self.user)
        self.url = reverse("order:v2:admin:order_list_create")

    def test_list_orders(self):
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 2)
        # Assuming you want to verify the details of the first order in the response
        expected_response = {
            "id": self.order1.id,
            "address": self.order1.address,
            "status": self.order1.status,
        }
        expected_order_item_response = {
            "order_items": [
                {
                    "id": self.order1_item1.id,
                    "code": self.order1_item1.code,
                    "name": self.order1_item1.name,
                    "price": self.order1_item1.price,
                    "amount": self.order1_item1.amount,
                    "unit": self.order1_item1.unit,
                    "comment": self.order1_item1.comment,
                    "status": self.order1_item1.status,
                    "order": self.order1_item1.order.id,
                    "product": self.order1_item1.product.id,
                },
                {
                    "id": self.order1_item2.id,
                    "code": self.order1_item2.code,
                    "name": self.order1_item2.name,
                    "price": self.order1_item2.price,
                    "amount": self.order1_item2.amount,
                    "unit": self.order1_item2.unit,
                    "comment": self.order1_item2.comment,
                    "status": self.order1_item2.status,
                    "order": self.order1_item2.order.id,
                    "product": self.order1_item2.product.id,
                },
            ],
        }
        pdb.set_trace()
        # self.assertDictContainsSubset(expected_response, response.data[0])
