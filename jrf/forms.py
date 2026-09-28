from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    confirm_email = forms.EmailField(label="Confirm Email")

    class Meta:
        model = Enquiry
        fields = [
            'first_name', 'last_name',
            'email', 'confirm_email',
            'address_line1', 'city', 'state',
            'phone',
            'description',
            'reason',
            'property_type',
            'attachment',
        ]
        widgets = {
            'reason': forms.RadioSelect,
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Please provide a brief description of your project.',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove Django's auto-inserted blank choice so only real options show
        self.fields['reason'].choices = Enquiry.REASON_CHOICES
        self.fields['reason'].widget = forms.RadioSelect(choices=Enquiry.REASON_CHOICES)

        self.order_fields([
            'first_name', 'last_name',
            'address_line1', 'city', 'state',
            'email', 'confirm_email',
            'phone',
            'description',
            'reason',
            'property_type',
            'attachment',
        ])

    def clean(self):
        ...  # unchanged
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        if email and confirm_email and email.lower() != confirm_email.lower():
            self.add_error('confirm_email', "Emails don't match.")
        return cleaned_data