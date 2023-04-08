from builtins import all

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from easy_thumbnails.files import get_thumbnailer

from main.forms import AddTestForm
from main.models import TestModel, QuestionsType1Model, QuestionsType2Model, QuestionsType3Model


def index(request):
    if request.method == 'POST':
        form = AddTestForm(request.POST)
        if form.is_valid():
            test = TestModel()
            test.surname_name = form.cleaned_data["surname_name"]
            test.group_number = form.cleaned_data["group_number"]
            test.number_of_questions = form.cleaned_data["number_of_questions"]
            subjects = get_subjects_list(form)
            questions_for_subjects_list = split_questions(test.number_of_questions, len(subjects))
            questions_types = 3  # types of questions in the database
            questions_json_dict = {'questions': {}}
            all_questions_type1 = QuestionsType1Model.objects.all()
            all_questions_type2 = QuestionsType2Model.objects.all()
            all_questions_type3 = QuestionsType3Model.objects.all()
            add_question_number = 1
            for i in range(len(subjects)):
                subject_number = subjects[i]
                questions_in_subject = questions_for_subjects_list[i]
                questions_for_questiontype_list = split_questions(questions_in_subject, questions_types)
                add_type1 = 0

                if all_questions_type2.filter(subject__subject_number=subject_number).count() >= \
                        questions_for_questiontype_list[1]:
                    questions_type2 = all_questions_type2.filter(subject__subject_number=subject_number).order_by('?')[
                                      :questions_for_questiontype_list[1]]
                else:
                    add_type1 += questions_for_questiontype_list[1] - all_questions_type2.filter(
                        subject__subject_number=subject_number).count()
                    questions_type2 = all_questions_type2.filter(subject__subject_number=subject_number).order_by('?').all()
                if all_questions_type3.filter(subject__subject_number=subject_number).count() >= \
                        questions_for_questiontype_list[2]:
                    questions_type3 = all_questions_type3.filter(subject__subject_number=subject_number).order_by('?')[
                                      :questions_for_questiontype_list[2]]
                else:
                    add_type1 += questions_for_questiontype_list[2] - all_questions_type3.filter(
                        subject__subject_number=subject_number).count()
                    questions_type3 = all_questions_type3.filter(subject__subject_number=subject_number).order_by('?').all()

                questions_type1 = all_questions_type1.filter(subject__subject_number=subject_number).order_by('?')[
                                  :questions_for_questiontype_list[0] + add_type1]
                # ...add other types

                for que in questions_type1:
                    questions_json_dict['questions'][add_question_number] = set_question_dict(1, que.id)
                    add_question_number += 1
                for que in questions_type2:
                    questions_json_dict['questions'][add_question_number] = set_question_dict(2, que.id)
                    add_question_number += 1
                for que in questions_type3:
                    questions_json_dict['questions'][add_question_number] = set_question_dict(3, que.id)
                    add_question_number += 1

            test.questions = questions_json_dict
            test.save()
            return redirect('test/1')
    else:
        form = AddTestForm()
    return render(request, 'main/index.html', {'form': form})


def viewquestion(request, question_number):
    test = TestModel.objects.latest('id')
    question_settings_dict = test.questions['questions'][str(question_number)]
    question_type = question_settings_dict['type']
    question_model = get_question_model(question_settings_dict, question_type)
    answer_options_dict = {}
    for i in range(len(question_model.answer_options)):
        answer_options_dict[i + 1] = question_model.answer_options[i]

    if request.method == 'POST':
        answer = int(request.POST.get("RadioOptions") if request.POST.get("RadioOptions") else 0)
        if answer == question_model.right_answer:
            if not test.questions['questions'][str(question_number)]['answered']:
                test.number_of_answered_questions += 1
                test.number_of_correctly_answered_questions += 1
                test.questions['questions'][str(question_number)]['answered'] = True
                test.questions['questions'][str(question_number)]['right'] = True
                test.save()
            question_settings_dict = test.questions['questions'][str(question_number)]
            data = {'test_data': test,
                    'progress_correct': percents(test.number_of_correctly_answered_questions, test.number_of_questions, progressbar=True),
                    'progress_wrong': percents(test.number_of_incorrectly_answered_questions, test.number_of_questions, progressbar=True),
                    'question': question_model,
                    'question_number': question_number,
                    'next_question_number': question_number + 1,
                    'answer_options_dict': answer_options_dict,
                    'question_settings_dict': question_settings_dict,
                    'user_answer': answer
                    }
            return render(request, f'main/current_question_type{question_type}.html', data)
        else:
            if not test.questions['questions'][str(question_number)]['answered']:
                test.number_of_answered_questions += 1
                test.number_of_incorrectly_answered_questions += 1
                test.questions['questions'][str(question_number)]['answered'] = True
                test.questions['questions'][str(question_number)]['right'] = False
                test.save()
            question_settings_dict = test.questions['questions'][str(question_number)]
            data = {'test_data': test,
                    'progress_correct': percents(test.number_of_correctly_answered_questions, test.number_of_questions, progressbar=True),
                    'progress_wrong': percents(test.number_of_incorrectly_answered_questions, test.number_of_questions, progressbar=True),
                    'question': question_model,
                    'question_number': question_number,
                    'next_question_number': question_number + 1,
                    'answer_options_dict': answer_options_dict,
                    'question_settings_dict': question_settings_dict,
                    'user_answer': answer
                    }
            return render(request, f'main/current_question_type{question_type}.html', data)
    else:
        data = {'test_data': test,
                'progress_correct': percents(test.number_of_correctly_answered_questions, test.number_of_questions, progressbar=True),
                'progress_wrong': percents(test.number_of_incorrectly_answered_questions, test.number_of_questions, progressbar=True),
                'question': question_model,
                'question_number': question_number,
                'next_question_number': question_number + 1,
                'answer_options_dict': answer_options_dict,
                'question_settings_dict': question_settings_dict
                }
        return render(request, f'main/current_question_type{question_type}.html', data)


def viewresults(request):
    test = TestModel.objects.latest('id')
    test.completed = True
    test.save()

    number_of_unanswered_questions = test.number_of_questions - test.number_of_answered_questions
    number_of_correctly_answered_questions = test.number_of_correctly_answered_questions
    number_of_incorrectly_answered_questions = test.number_of_incorrectly_answered_questions
    result = percents(number_of_correctly_answered_questions, test.number_of_questions)

    data = {
        'number_of_correctly_answered_questions': number_of_correctly_answered_questions,
        'number_of_incorrectly_answered_questions': number_of_incorrectly_answered_questions,
        'number_of_unanswered_questions': number_of_unanswered_questions,
        'surname_name': test.surname_name,
        'group_number': test.group_number,
        'result': result,
        'incorrectly_answered_questions': incorrectly_answered_questions()
    }
    return render(request, 'main/Results.html', data)


def about(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    data = {
        'return_path': return_path
    }
    return render(request, 'main/about.html', data)


def author(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    data = {
        'return_path': return_path
    }
    return render(request, 'main/author.html', data)


def bober(request):
    test = TestModel.objects.latest('id')
    questions_settings = test.questions['questions']
    bober_alive = []
    qe_answer = 0
    for i in range(1, test.number_of_questions + 1):
        qe_type = questions_settings[str(i)]['type']
        qe_id = questions_settings[str(i)]['id']
        if qe_type == 1:
            qe_answer = QuestionsType1Model.objects.get(id=qe_id).right_answer
        if qe_type == 2:
            qe_answer = QuestionsType2Model.objects.get(id=qe_id).right_answer
        if qe_type == 3:
            qe_answer = QuestionsType3Model.objects.get(id=qe_id).right_answer
        bober_alive.append((i, qe_answer))
    return render(request, 'main/bober.html', {'bober_alive': bober_alive})


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
                list_of_questions.append(pp + 1)
            else:
                list_of_questions.append(pp)
        list_of_questions.reverse()
        return list_of_questions


def percents(qe_part, qe_all, progressbar=False):
    out_percents = round(100 / qe_all * qe_part, 1)
    if progressbar:
        return str(out_percents).replace(',', '.')
    else:
        return out_percents


def set_question_dict(type_number, que_id):
    return {'type': type_number,
            'id': que_id,
            'answered': False,
            'right': None
            }


def get_subjects_list(form):
    test_type = form.cleaned_data["test_type"]
    if test_type == '2':
        subjects = [1, 2, 3, 4, 5, 6]
    elif test_type == '3':
        subjects = [7, 8, 9]
    elif test_type == '4':
        subjects = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    else:
        subjects = form.cleaned_data["check_subjects"]
    return subjects


def get_question_model(question_settings_dict, question_type):
    question_id = question_settings_dict['id']
    if question_type == 1:
        question_model = QuestionsType1Model.objects.get(id=question_id)
    elif question_type == 2:
        question_model = QuestionsType2Model.objects.get(id=question_id)
    else:
        question_model = QuestionsType3Model.objects.get(id=question_id)
    return question_model


def incorrectly_answered_questions():
    questions = TestModel.objects.latest('id').questions['questions']
    answered_questions_list = []
    for key in questions:
        if questions[key]['right'] == False:
            answered_questions_list.append(key)
    return answered_questions_list


@login_required
def file_handler(request):
    if request.method == 'POST':
        file = request.FILES['file']
        directory_name = 'img_for_type2/' + file.name
        options = {'autocrop': True, 'size': (0, 80), 'detail': True, 'quality': 100}
        thumb = get_thumbnailer(file, relative_name=directory_name).get_thumbnail(options, save=True)
        return JsonResponse({'value': thumb.url})
    # elif request.method == 'DELETE':
    #     trigger = request.GET.get('trigger')
    #     file_names = request.GET.getlist('value')
    #     if trigger != 'delete_button':
    #         return HttpResponse(status=200)
    #     for name in file_names:
    #         fs.delete(name)
    #     return HttpResponse(status=200)  # success
