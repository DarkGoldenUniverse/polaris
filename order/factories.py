import factory

from account.factories import UserFactory
from customer.factories import CustomerFactory
from inventory.factories import InventoryFactory
from order.models import Order, OrderItem


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    address = factory.Faker("address")

    # Define related factories
    customer = factory.SubFactory(CustomerFactory)
    creator = factory.SubFactory(UserFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    amount = factory.Faker("pydecimal", left_digits=2, right_digits=3, positive=True, min_value=10, max_value=99)

    # Define related factories
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(InventoryFactory, executed_amount=0, amount=amount, visible=True)
    executor = factory.SubFactory(UserFactory)
    creator = factory.SubFactory(UserFactory)
