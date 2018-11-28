from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


class Payment(models.Model):

    enrollment          = models.ForeignKey("Enrollment", blank=True, null=True)
    payment_type        = models.ForeignKey("PaymentType", blank=True, null=True)
    amount_paid         = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=8)
    official_receipt_no = models.CharField(max_length=15, blank=True, null=True)
    enrollment_form_no  = models.CharField(max_length=15, blank=True, null=True)
    payment_date        = models.DateTimeField(default=timezone.now, blank=True, null=True)
    created_on          = models.DateField(blank=False, null=False, default=timezone.now)
    is_deleted          = models.BooleanField(default=False)
    company             = models.ForeignKey("Company")

    class Meta:
        app_label = "systech_account"
        db_table  = "payments"
        ordering  = ["id"]


class PaymentType(models.Model):
    
    name        = models.CharField(max_length=20, blank=False, null=False)
    is_active   = models.BooleanField(default=True)
    is_deleted  = models.BooleanField(default=False)
    company     = models.ForeignKey("Company")

    class Meta:
        app_label = "systech_account"
        db_table  = "payment_types"
        ordering  = ["id"]
