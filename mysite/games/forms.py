from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

def all_number(value):
    if not value.isdigit():
        raise ValidationError(
            _(f'{value} is not just numbers'), code="invalid")

        # raise ValidationError(_('%(value)s is not just numbers'), params={"value": value}, code="invalid")


class SolveSudokuForm(forms.Form):
    square = forms.DecimalField(
        min_value=0, max_value=9, max_digits=1, required=False, initial=Decimal(0))
