from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (  'full_name', 'email', 'phone_number', 'country',
                    'postcode', 'town_or_city', 'street_address1',
                    'street_address2', 'county')
    
    def __init__(self, *args, **kwargs):  # Override init method to add placeholders and classes, remove auto-generated labels and set autofocus on first field 
                                            # this is  Django form best practice to ensure the form is user-friendly and visually consistent with the rest of the site.
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = { # Define placeholders for each field
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True         # Set autofocus on first field
        for field in self.fields:                                       # Loop through fields to add placeholders and classes, and remove labels
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False