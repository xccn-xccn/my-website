from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import formset_factory

def all_number(value):
    if not value.isdigit():
        raise ValidationError(
            _(f'{value} is not just numbers'), code="invalid")

        # raise ValidationError(_('%(value)s is not just numbers'), params={"value": value}, code="invalid")

def validate_sudoku(puzzle):
    sections, rows, columns = [{k: set() for k in range(9)} for _ in range(3)]
    if len(puzzle) != 9:
        raise ValidationError(_("Sudoku Has Wrong Dimensions"))
    for y, line in enumerate(puzzle):
        for x, num in enumerate(line):
            if len(puzzle) != 9:
                raise ValidationError(_("Sudoku Has Wrong Dimensions"))
            elif num > 9 or num < 0 or num in rows[y] or num in columns[x] or num in sections[x//3 + (y//3)*3]:
                raise ValidationError(_("Invalid Sudoku"))
            else:
                rows[y].add(num)
                columns[x].add(num)
                sections[x//3 + (y//3)*3].add(num)
    return True


class SolveSudokuForm(forms.Form):
    # template_name = "games/sudoku_form_render.html"
    square = forms.DecimalField(
        min_value=0, 
        max_value=9, 
        max_digits=1, 
        required=False, 
        label="",
        widget=forms.NumberInput(attrs={'class': 'sudoku-cell'})
    )


SudokuFormSet = formset_factory(SolveSudokuForm, extra=81)


class SudokuFormsetValid(SudokuFormSet):
    def clean(self):
        super().clean()

        puzzle = [[] for _ in range(9)]
        for count, square in enumerate(self.forms):
            puzzle[count // 9].append(square)
        sections, rows, columns = [{k: set() for k in range(9)} for _ in range(3)]
        if len(puzzle) != 9:
            raise ValidationError(_("Sudoku Has Wrong Dimensions"))
        for y, line in enumerate(puzzle):
            for x, square in enumerate(line):
                num = square.cleaned_data.get("square", 0)
                if len(puzzle) != 9:
                    raise ValidationError(_("Sudoku Has Wrong Dimensions"))
                if num == 0:
                    continue
                elif num > 9 or num < 0 or num in rows[y] or num in columns[x] or num in sections[x//3 + (y//3)*3]:
                    for field in square:
                        print(type(field), "/n/n")
                        field.widget.attrs['class'] += 'is-invalid'
                    raise ValidationError(_("Invalid Sudoku"))
                else:
                    rows[y].add(num)
                    columns[x].add(num)
                    sections[x//3 + (y//3)*3].add(num)



class QuickEnterForm(forms.Form):
    sudoku = forms.CharField(max_length=81, min_length=81, label="Quick Enter")

#483921657967345821251876493548132976729564138136798245372689514814253769695417382