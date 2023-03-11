from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def all_number(value):
    if not value.isdigit():
        raise ValidationError(_(f'{value} is not just numbers'))

        # raise ValidationError(_('%(value)s is not just numbers'), params={"value": value})
    

class SolveSudokuForm(forms.Form):
    line_1 = forms.CharField(label="Row one", max_length=9, help_text="max length of 9", validators=[all_number])


