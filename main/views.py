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
            test.number_of_questions = form.cleaned_data["number_of_questions"]
            test_type = form.cleaned_data["test_type"]
            subjects = []
            if test_type == '2':
                subjects = [1, 2, 3, 4, 5]
            elif test_type == '3':
                subjects = [6, 7, 8, 9, 10]
            else:
                subjects = form.cleaned_data["check_subjects"]
                    #print(subjects)
                    #print(test.number_of_questions)
            questions_for_subjects_list = split_questions(test.number_of_questions, len(subjects))
                #print(questions_for_subjects_list)
            questions_types = 3
            questions_json_dict = {'questions': {}}
            for i in range(len(subjects)):
                subject_number = subjects[i]
                questions_in_subject = questions_for_subjects_list[i]
                questions_for_question_type_list = split_questions(questions_in_subject, questions_types)
                    #print(questions_for_question_type_list)
    else:
        form = AddTestForm()
    return render(request, 'main/index.html', {'form': form})

def split_questions(x, n):
    if x < n:
        list_of_questions = [0] * n
        for i in range(x):
            list_of_questions[i] = 1
        return list_of_questions
    elif x % n == 0:
        list_of_questions = [x // n for i in range(n)]
        return list_of_questions
    else:
        list_of_questions = []
        zp = n - (x % n)
        pp = x // n
        for i in range(n):
            if i >= zp:
                list_of_questions.append(pp+1)
            else:
                list_of_questions.append(pp)
        list_of_questions.reverse()
        return list_of_questions