import random

import factory

from inventory.models import Store, Category, Inventory


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Sequence(lambda n: f"store_{n:02d}")


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"category_{n:02d}")


class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Inventory

    name = factory.Sequence(lambda n: f"product_{n:02d}")
    code = factory.Sequence(lambda n: f"p{n:09d}")
    visible = factory.Faker("boolean", chance_of_getting_true=50)

    max_price = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True, min_value=10, max_value=100)
    price = factory.Faker("pydecimal", left_digits=6, right_digits=2, positive=True, min_value=10, max_value=max_price)

    executed_amount = factory.Faker(
        "pydecimal", left_digits=5, right_digits=3, positive=True, min_value=100, max_value=1000
    )
    amount = factory.Faker(
        "pydecimal", left_digits=5, right_digits=3, positive=True, min_value=executed_amount, max_value=2000
    )
    unit = factory.LazyFunction(lambda: random.choice(["kg", "g", "l", "ml"]))

    # Define related factories
    store = factory.SubFactory(StoreFactory)
    category = factory.SubFactory(CategoryFactory)
