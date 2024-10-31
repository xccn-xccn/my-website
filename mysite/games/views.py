from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .forms import SolveSudokuForm, QuickEnterForm, SudokuFormsetValid
from .utility import solve_sudoku, valid_sudoku


def home(request):
    context = {

    }
    return render(request, "games/home.html", context)

# def QuickEnterFunc(request):
#     if request == "POST":
#         QuickEnter = QuickEnterForm(request.POST)
#         if QuickEnter.is_valid():
#             SudokuFormSet = formset_factory(SolveSudokuForm, extra=0)
#             print("".join(QuickEnter.cleaned_data["sudoku"].split()), len("".join(QuickEnter.cleaned_data["sudoku"].split())))
#             SudokuForm = SudokuFormSet(initial=[{"square": value} for value in "".join(QuickEnter.cleaned_data["sudoku"].split())])
#             return render(request, "games/sudoku.html", {"sudoku_forms": SudokuForm})
#         else:
#             print("invalid quickenter", QuickEnter.errors)
#             for error in QuickEnter.errors:
#                 messages.error(request, "Invalid quick-enter")
#     return render(request,"games/sudoku.html", {"quick_enter": QuickEnterForm()})

# cd .\Documents\programming\my-website\mysite\
def sudoku(request):  # TODO   if decimal number, allow spaces in quick enter, make input red but new same, make copy quick enter, make generator,
    SudokuFormSet = formset_factory(SolveSudokuForm, extra=81)
    SudokuForm = SudokuFormSet()
    QuickEnter = QuickEnterForm()
    context = {

    }
    context["solved"] = "NO"
    if request.method == "POST":
        if "sudoku_submit" in request.POST:
            print("sudoku_submited")
            SudokuForm = SudokuFormSet(request.POST)
            print("form with validation created")
            if SudokuForm.is_valid():
                SudokuForm, valid = valid_sudoku(SudokuForm)
                if valid:
                    result = solve_sudoku(SudokuForm)
                    messages.success(request, "Sudoku Solved")
                    context["solved_sudoku"] = result
                else:
                    messages.error(request, "Invalid Sudoku")
            else:
                messages.error(request, "Invalid Sudoku")
        elif "quick_enter" in request.POST:
            print("quick entered")
            QuickEnter = QuickEnterForm(request.POST)
            if QuickEnter.is_valid():
                SudokuFormSet = formset_factory(SolveSudokuForm, extra=0)
                print("".join(QuickEnter.cleaned_data["sudoku"].split()), len("".join(QuickEnter.cleaned_data["sudoku"].split())))
                SudokuForm = SudokuFormSet(initial=[{"square": value} for value in "".join(QuickEnter.cleaned_data["sudoku"].split())])

    else:
        print("no post")
        
    context["sudoku_forms"] = SudokuForm
    context["quick_enter"] = QuickEnter
    return render(request, "games/sudoku.html", context)

