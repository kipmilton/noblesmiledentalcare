from django import forms
from .models import Appointment
from .models import UserProfile


class ProofOfPaymentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['proof_of_payment']
        widgets = {
            'proof_of_payment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class AppointmentForm(forms.ModelForm): 
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'department', 'doctor', 'message']




class RegistrationFormm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ['username', 'password', 'contact_number', 'email', 'address']

    # Custom validation for password confirmation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data