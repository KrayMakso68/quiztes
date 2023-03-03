from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.http import Http404
from main.forms import AddTestForm
from main.models import TestModel, QuestionsType1Model, QuestionsType2Model, QuestionsType3Model, QuestionsType4Model


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
            elif test_type == '4':
                subjects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            else:
                subjects = form.cleaned_data["check_subjects"]
                print(subjects)
                print(test.number_of_questions)
            questions_for_subjects_list = split_questions(test.number_of_questions, len(subjects))
            print(questions_for_subjects_list)
            questions_types = 1                # types of questions in the database
            questions_json_dict = {'questions': {}}
            all_questions_type1 = QuestionsType1Model.objects.all()
            #all_questions_type2 = QuestionsType2Model.objects.all()
            #all_questions_type3 = QuestionsType3Model.objects.all()
            #all_questions_type4 = QuestionsType4Model.objects.all()
            add_question_number = 1
            for i in range(len(subjects)):
                subject_number = subjects[i]
                questions_in_subject = questions_for_subjects_list[i]
                questions_for_questiontype_list = split_questions(questions_in_subject, questions_types)
                print(questions_for_questiontype_list)
                questions_type1 = all_questions_type1.filter(subject__subject_number=subject_number).order_by('?')[:questions_for_questiontype_list[0]]
                #questions_type2 = all_questions_type2.filter(subject__subject_number=subject_number).order_by('?')[:questions_for_questiontype_list[1]]
                #questions_type3 = all_questions_type3.filter(subject__subject_number=subject_number).order_by('?')[:questions_for_questiontype_list[2]]
                #questions_type4 = all_questions_type4.filter(subject__subject_number=subject_number).order_by('?')[:questions_for_questiontype_list[3]]
                # ...add other types

                for que in questions_type1:
                    questions_json_dict['questions'][add_question_number] = {'type': '1',
                                                                             'id': que.id,
                                                                             'answered': False,
                                                                             'right': None
                                                                             }
                    add_question_number += 1
                # for que in questions_type2:
                #     questions_json_dict['questions'][add_question_number] = {'type': '2',
                #                                                              'id': que.id,
                #                                                              'answered': False,
                #                                                              'right': None
                #                                                              }
                #     add_question_number += 1
                # for que in questions_type3:
                #     questions_json_dict['questions'][add_question_number] = {'type': '3',
                #                                                              'id': que.id,
                #                                                              'answered': False,
                #                                                              'right': None
                #                                                              }
                #     add_question_number += 1
                # for que in questions_type4:
                #     questions_json_dict['questions'][add_question_number] = {'type': '4',
                #                                                              'id': que.id,
                #                                                              'answered': False,
                #                                                              'right': None
                #                                                              }
                #     add_question_number += 1
            test.questions = questions_json_dict
            test.save()
            return redirect('test/1')
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
                list_of_questions.append(pp + 1)
            else:
                list_of_questions.append(pp)
        list_of_questions.reverse()
        return list_of_questions

def percents(qe_part, qe_all):
    qe_part = int(qe_part)
    qe_all = int(qe_all)
    out = int(100 / qe_all * qe_part)
    print(out)
    return out


def viewquestion(request, question_number):
    test = TestModel.objects.latest('id')
    question_settings_dict = test.questions['questions'][str(question_number)]
    question_type = question_settings_dict['type']
    question_id = question_settings_dict['id']
    question_answered_check = question_settings_dict['answered']
    question_right_check = question_settings_dict['right']

    question_model = None
    if question_type == '1':
        question_model = QuestionsType1Model.objects.get(id=question_id)
    elif question_type == '2':
        question_model = QuestionsType2Model.objects.get(id=question_id)
    elif question_type == '3':
        question_model = QuestionsType3Model.objects.get(id=question_id)
    else:
        question_model = QuestionsType4Model.objects.get(id=question_id)

    answer_options_dict = {}
    for i in range(len(question_model.answer_options)):
        answer_options_dict[(i+1)] = question_model.answer_options[i]

    if request.method == 'POST':
        answer = request.POST.get("RadioOptions") if request.POST.get("RadioOptions") else '0'
        if str(answer) == str(question_model.right_answer):
            if not test.questions['questions'][str(question_number)]['answered']:
                test.number_of_answered_questions += 1
                test.number_of_correctly_answered_questions += 1
                test.questions['questions'][str(question_number)]['answered'] = True
                test.questions['questions'][str(question_number)]['right'] = True
                test.save()
            question_settings_dict = test.questions['questions'][str(question_number)]
            data = {'test_data': test,
                    'progress_correct': percents(test.number_of_correctly_answered_questions, test.number_of_questions),
                    'progress_wrong': percents(test.number_of_incorrectly_answered_questions, test.number_of_questions),
                    'question': question_model,
                    'question_number': question_number,
                    'next_question_number': question_number + 1,
                    'answer_options_dict': answer_options_dict,
                    'question_settings_dict': question_settings_dict,
                    'user_answer': int(answer)
                    }
            return render(request, 'main/current_question_type1.html', data)
        else:
            if not test.questions['questions'][str(question_number)]['answered']:
                test.number_of_answered_questions += 1
                test.number_of_incorrectly_answered_questions += 1
                test.questions['questions'][str(question_number)]['answered'] = True
                test.questions['questions'][str(question_number)]['right'] = False
                test.save()
            question_settings_dict = test.questions['questions'][str(question_number)]
            data = {'test_data': test,
                    'progress_correct': percents(test.number_of_correctly_answered_questions, test.number_of_questions),
                    'progress_wrong': percents(test.number_of_incorrectly_answered_questions, test.number_of_questions),
                    'question': question_model,
                    'question_number': question_number,
                    'next_question_number': question_number + 1,
                    'answer_options_dict': answer_options_dict,
                    'question_settings_dict': question_settings_dict,
                    'user_answer': int(answer)
                    }
            return render(request, 'main/current_question_type1.html', data)
    else:
        data = {'test_data': test,
                'progress_correct': percents(test.number_of_correctly_answered_questions, test.number_of_questions),
                'progress_wrong': percents(test.number_of_incorrectly_answered_questions, test.number_of_questions),
                'question': question_model,
                'question_number': question_number,
                'next_question_number': question_number + 1,
                'answer_options_dict': answer_options_dict,
                'question_settings_dict': question_settings_dict
                }
        return render(request, 'main/current_question_type1.html', data)
