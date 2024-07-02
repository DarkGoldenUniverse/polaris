# Generated by Django 5.0.6 on 2024-07-02 22:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.CharField(choices=[('0', 'pending'), ('1', 'in_progress'), ('2', 'delivered'), ('3', 'cancelled')], default='0', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_created_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'orders',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, editable=False, max_length=10)),
                ('name', models.CharField(blank=True, editable=False, max_length=50)),
                ('unit', models.CharField(blank=True, editable=False, max_length=5)),
                ('price', models.DecimalField(decimal_places=2, editable=False, max_digits=8)),
                ('amount', models.DecimalField(decimal_places=3, default=0, editable=False, max_digits=8)),
                ('comment', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('0', 'pending'), ('1', 'in_progress'), ('2', 'completed'), ('3', 'cancelled')], default='0', max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assign_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item_assign_to', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item_created_by', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='inventory.inventory')),
            ],
            options={
                'verbose_name_plural': 'order items',
                'ordering': ['-created_at'],
            },
        ),
    ]
