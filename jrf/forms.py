from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    confirm_email = forms.EmailField(label="Confirm Email")
    captcha_answer = forms.IntegerField(label="Custom Captcha")

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

    def __init__(self, *args, captcha_a=None, captcha_b=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.captcha_a = captcha_a
        self.captcha_b = captcha_b
        if captcha_a is not None and captcha_b is not None:
            self.fields['captcha_answer'].label = f"What is {captcha_a} + {captcha_b}?"

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
            'captcha_answer',
        ])

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')
        if email and confirm_email and email.lower() != confirm_email.lower():
            self.add_error('confirm_email', "Emails don't match.")
        return cleaned_data

    def clean_captcha_answer(self):
        answer = self.cleaned_data.get('captcha_answer')
        if self.captcha_a is None or self.captcha_b is None:
            raise forms.ValidationError("Captcha expired, please try again.")
        if answer != self.captcha_a + self.captcha_b:
            raise forms.ValidationError("That answer isn't correct.")
        return answer