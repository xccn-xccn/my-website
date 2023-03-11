from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SolveSudokuForm
# Create your views here.

def home(request):
    context = {

    }
    return render(request, "games/home.html", context)


def sudoku(request):
    context = {

    }
    if request.method == "POST":
        form = SolveSudokuForm(request.POST)

        if form.is_valid():
            messages.success(request, "yay")
            return redirect(sudoku)
    else:
        form = SolveSudokuForm()
    return render(request, "games/sudoku.html", {"form": form})