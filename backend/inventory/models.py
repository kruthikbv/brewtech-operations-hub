from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from common.constants import STOCK_IN, STOCK_OUT

class InventoryItem(models.Model):
    CATEGORY_CHOICES = [(value, value.replace('_', ' ').title()) for value in ['BEVERAGE_INGREDIENT', 'CONSUMABLE', 'MACHINE_SUPPLY', 'CLEANING_SUPPLY', 'OTHER']]

    item_code = models.CharField(max_length=30, unique=True, db_index=True)
    item_name = models.CharField(max_length=200, db_index=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, db_index=True)
    current_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'), validators=[MinValueValidator(Decimal('0'))])
    unit = models.CharField(max_length=30)
    minimum_stock_level = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0'), validators=[MinValueValidator(Decimal('0'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(current_quantity__gte=0), name='inventory_quantity_nonnegative'),
            models.CheckConstraint(condition=models.Q(minimum_stock_level__gte=0), name='inventory_minimum_nonnegative'),
        ]
    @property
    def is_low_stock(self) -> bool: return self.current_quantity <= self.minimum_stock_level

class InventoryTransaction(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=[(STOCK_IN, 'Stock In'), (STOCK_OUT, 'Stock Out')])
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    transaction_date = models.DateField()
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [models.Index(fields=['inventory_item', 'transaction_date'])]
