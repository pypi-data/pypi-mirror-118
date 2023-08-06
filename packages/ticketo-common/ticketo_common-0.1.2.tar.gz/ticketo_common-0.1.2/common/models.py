import uuid
from decimal import Decimal
from ool import VersionField, VersionedMixin
from django.core.validators import MinValueValidator
from django.db import models


class TicketBase(VersionedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Title', max_length=50)
    price = models.DecimalField('Price', max_digits=10, decimal_places=4,
                                validators=[MinValueValidator(Decimal('0.01'))])
    version = VersionField()

    class Meta:
        abstract = True
