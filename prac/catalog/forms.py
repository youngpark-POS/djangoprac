from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks(default 3).")

    # default clean method: clean_<fieldname>
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < date.today():
            raise ValidationError(_("Invalid date - renewal in past"))
        
        if data > date.today() + timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))
        
        return data