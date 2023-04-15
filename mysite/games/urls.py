from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path("sudoku/quick_enter", views.QuickEnter, name="quickenter"),
    path("sudoku/", views.sudoku, name="sudoku")
]