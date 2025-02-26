from django import forms
from django.contrib import admin
from .models import PreviewRequest

class PreviewRequestForm(forms.ModelForm):
    class Meta:
        model = PreviewRequest
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['approved_by'].queryset = self.fields['approved_by'].queryset.filter(is_superuser=True)

@admin.register(PreviewRequest)
class PreviewRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'document', 'is_approved', 'approved_by', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('requester__username', 'document__document_name', 'approved_by__username')
    form = PreviewRequestForm

