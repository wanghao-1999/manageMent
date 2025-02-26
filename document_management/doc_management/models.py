# doc_management/models.py


from django.conf import settings
from django.db import models


class Document(models.Model):
    CONTRACT_CATEGORY_CHOICES = (
        ('paper', '纸质文档'),
        ('electronic', '电子文档'),
    )

    document_type = models.CharField(max_length=100)
    document_name = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document_file = models.FileField(upload_to='documents/')

    contract_signature_date = models.DateField(null=True, blank=True)
    contract_expiry_date = models.DateField(null=True, blank=True)
    contract_amount_with_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contract_amount_without_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_terms = models.ForeignKey('doc_management.PaymentTerm', on_delete=models.SET_NULL, null=True, blank=True)

    contract_category = models.CharField(max_length=20, choices=CONTRACT_CATEGORY_CHOICES, default='paper')

    def __str__(self):
        return self.document_name


class PreviewRequest(models.Model):
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='approved_requests', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Preview request by {self.requester} for {self.document}"


class PaymentTerm(models.Model):
    abbreviation = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.abbreviation
