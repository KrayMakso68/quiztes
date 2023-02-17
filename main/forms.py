from django import forms
from django.forms import ValidationError

from main.models import Subject


class AddTestForm(forms.Form):
    check_subjects_choices = ((subject.subject_number, subject.name) for subject in Subject.objects.all())
    test_type_choices = (
        (1, 'Свой тест'),
        (2, 'Тест за 4 семестр'),
        (3, 'Тест за 5 семестр'),
        (4, 'Тест за курс обучения'),
    )

    surname_name = forms.CharField(required=True, max_length=50)
    surname_name.widget = forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'floatingInput',
        'placeholder': 'Фамилия Имя'
    })
    group_number = forms.IntegerField(required=True, min_value=101, max_value=1000)
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
        validators=[],
        choices=check_subjects_choices,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input',
            'name': 'checkbox',
            'type': 'checkbox',
            'id': 'flexCheck'
        }),
    )
    number_of_questions = forms.IntegerField(required=True, min_value=1, max_value=200)
    number_of_questions.widget = forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'CountQuestions',
        'placeholder': 'Количество вопросов'
    })

    def clean(self):
        super(AddTestForm, self).clean()
        if self.cleaned_data['test_type'] == '1' and not self.cleaned_data['check_subjects']:
            raise ValidationError('Для своего теста необходимо выбрать темы')

    def clean_surname_name(self):
        name = self.cleaned_data['surname_name']
        words_number = len(name.split())
        if words_number != 2:
            raise ValidationError(f'Фамилия и Имя это 2 слова, а не {words_number}!')
