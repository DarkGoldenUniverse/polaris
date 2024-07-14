import factory

from customer.models import Customer, Address


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Sequence(lambda n: f"customer_{n}")
    phone_number = factory.Sequence(lambda n: f"12345{n:05d}")


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address = factory.Faker("address")

    # Define a related factory
    customer = factory.SubFactory(CustomerFactory)
