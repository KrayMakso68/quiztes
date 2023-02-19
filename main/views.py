from django.shortcuts import render
from django.http import HttpResponse
from main.forms import AddTestForm
from main.models import TestModel


def index(request):
    if request.method == 'POST':
        form = AddTestForm(request.POST)
        if form.is_valid():
            test = TestModel()
            test.surname_name = form.cleaned_data["surname_name"]
            test.group_number = form.cleaned_data["group_number"]
            test.number_of_questions = number_of_questions = form.cleaned_data["number_of_questions"]
            test_type = form.cleaned_data["test_type"]
            subjects = []
            if test_type == '2':
                subjects = [1, 2, 3, 4, 5]
            elif test_type == '3':
                subjects = [6, 7, 8, 9, 10]
            else:
                subjects = form.cleaned_data["check_subjects"]
                print(subjects)

    else:
        form = AddTestForm()
    return render(request, 'main/index.html', {'form': form})