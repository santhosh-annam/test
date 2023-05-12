from django import forms
import datetime
from ebanking.utils import is_date


class RegistrationForm(forms.Form):
    CARD_NUMBER_LENGTH = 16
    CPR_LENGTH = 18
    EXPIRY_LENGTH = 4
    yrs = [year for year in range(datetime.datetime.now().year, 1899, -1)]

    cpr = forms.CharField()
    card_number = forms.CharField()
    expiry = forms.CharField()
    dob = forms.DateField(widget=forms.widgets.SelectDateWidget(years=yrs))
    channel = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super().clean()
        cpr = cleaned_data.get("cpr")
        card_number = cleaned_data.get("card_number")
        expiry = cleaned_data.get("expiry")
        dob = cleaned_data.get("dob")

        # CPR validation
        if not cpr:
            self.add_error('cpr', "CPR should not be left blank")
        elif not isinstance(cpr, str) or len(cpr) > self.CPR_LENGTH:
            self.add_error('cpr', ("CPR should be upto " +
                                   str(self.CPR_LENGTH) + " digits only"))
        elif not cpr.isnumeric():
            self.add_error('cpr', "Invalid CPR")
        else:
            pass

        # CardNumber validation
        if isinstance(card_number, str):
            card_number = card_number.replace(" ", "")

        if not card_number:
            self.add_error('card_number',
                           ("Card number should not be left blank"))
        elif len(card_number) != self.CARD_NUMBER_LENGTH:
            self.add_error('card_number', ("Card number should have " +
                                           str(self.CARD_NUMBER_LENGTH) +
                                           " digits"))
        elif not card_number.isnumeric():
            self.add_error('card_number', "Invalid card number")
        else:
            pass

        # Expiry validation
        if not expiry:
            self.add_error('expiry', "Expiry should not be left blank")
        elif isinstance(expiry, str) and expiry.__contains__("/"):
            expiry_tokens = expiry.split("/")
            expiry = expiry_tokens[1] + expiry_tokens[0]
            if (len(expiry) != self.EXPIRY_LENGTH or
                    str(expiry) == "0000" or not expiry.isnumeric()):
                self.add_error('expiry', "Invalid expiry")
        else:
            self.add_error('expiry', "Expiry should be in MM/YY format")

        # DOB validation
        if not dob:
            self.add_error('dob', "Date of birth should not be left blank")
        elif not isinstance(dob, datetime.date) or not is_date(str(dob)):
            self.add_error('dob', "Invalid Date of birth")
        else:
            pass

        # Updating cleaned form data
        self.cleaned_data['card_number'] = card_number
        self.cleaned_data['expiry'] = expiry

        # print("Cleaned form data is : " + str(cleaned_data))
        return self.cleaned_data
