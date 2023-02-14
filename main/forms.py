from django import forms
from django.forms import TextInput, NumberInput, SelectMultiple

class AddTestForm(forms.Form):
    test_type_choices = (
        (1, 'Свой тест'),
        (2, 'Тест за 4 семестр'),
        (3, 'Тест за 5 семестр'),
        (4, 'Тест за курс обучения'),
    )
    check_subjects_choices = (
        (1, 'Тема №1'),
        (2, 'Тема №2'),
        (3, 'Тема №3'),
        (4, 'Тема №4'),
        (5, 'Тема №5'),
        (6, 'Тема №6'),
        (7, 'Тема №7'),
        (8, 'Тема №8'),
        (9, 'Тема №9'),
        (10, 'Тема №10')
    )

    surname_name = forms.CharField(max_length='50')
    surname_name.widget = forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'Фамилия Имя'
    })
    group_number = forms.IntegerField(min_value='101', max_value='1000')
    group_number.widget = forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'Номер учебной группы'
    })
    test_type = forms.ChoiceField(choices=test_type_choices, widget=forms.Select(attrs={
        'class': 'form-select  mb-4',
        'aria-label': '.form-select-sm'
    }))
    check_subjects = forms.MultipleChoiceField(
        choices=check_subjects_choices,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'name': 'checkbox',
            'type': 'checkbox',
            'id': 'flexCheck'
        }),
    )
    number_of_questions = forms.IntegerField(min_value='1', max_value='200')
    number_of_questions.widget = forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'CountQuestions',
        'placeholder': 'Количество вопросов'
    })