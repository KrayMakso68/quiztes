from django.db import models
from django_jsonform.models.fields import JSONField


class Subject(models.Model):
    name = models.CharField('Название', max_length=20)
    subject_number = models.IntegerField('Номер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class TestModel(models.Model):
    surname_name = models.CharField('Фамилия Имя', max_length=100)
    group_number = models.IntegerField('Номер группы')
    number_of_questions = models.IntegerField('Количество вопросов')
    number_of_answered_questions = models.IntegerField('Количестов отвеченных вопросов', default=0)
    number_of_correctly_answered_questions = models.IntegerField('Количестов правильно отвеченных вопросов', default=0)
    number_of_incorrectly_answered_questions = models.IntegerField('Количестов неправильно отвеченных вопросов', default=0)
    questions = models.JSONField('Вопросы теста')

    def __str__(self):
        return self.surname_name

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class QuestionsType1Model(models.Model):
    ITEMS_SCHEMA = {
        'type': 'list',
        'title': 'Варианты ответов',
        'items': {
            'type': 'string'
        },
        "minItems": 2,
        "maxItems": 6
    }
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
    text = models.TextField('Текст вопроса')
    answer_options = JSONField('Варианты ответов', schema=ITEMS_SCHEMA)
    right_answer = models.IntegerField('Номер верного ответа (по порядку)')

    class Meta:
        verbose_name = 'Вопрос 1 типа'
        verbose_name_plural = 'Вопросы 1 типа'

    def __str__(self):
        return self.subject.name + " | " + self.text


class QuestionsType2Model(models.Model):
    ITEMS_SCHEMA = {
        'type': 'list',
        'title': 'Варианты ответов с картинкой',
        'items': {
            'type': 'object',
            'keys': {
                "img_input": {  # в списке по ключу 'img_input' получим путь до файла по типу 'path/to/logo.png'
                    "type": "string",
                    "format": "file-url",
                    "widget": "fileinput",
                    "helpText": "Выберите изображение для загрузки",
                }
            }
        },
        "minItems": 2,
        "maxItems": 6
    }
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
    text = models.TextField('Текст вопроса')
    answer_options = JSONField('Варианты ответов', schema=ITEMS_SCHEMA,
                               help_text='Attention! Вырезайте изображения формул в примерно одинаковом масштабе!')
    right_answer = models.IntegerField('Номер верного ответа (по порядку)')

    class Meta:
        verbose_name = 'Вопрос 2 типа'
        verbose_name_plural = 'Вопросы 2 типа'

    def __str__(self):
        return self.subject.name + " | " + self.text


class QuestionsType3Model(models.Model):
    ITEMS_SCHEMA = {
        'type': 'list',
        'title': 'Варианты ответов',
        'items': {
            'type': 'string'
        },
        "minItems": 2,
        "maxItems": 6
    }
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
    text = models.TextField('Текст вопроса')
    image = models.ImageField('Изображение для вопроса', upload_to='img_for_type3/',
                              help_text='Attention! Для добавления формул при вырезании увеличивайте мастштаб! '
                                        'Изображения будут выводиться в том же масштабе, что вы и вырезали!')
    answer_options = JSONField('Варианты ответов', schema=ITEMS_SCHEMA)
    right_answer = models.IntegerField('Номер верного ответа (по порядку)')

    class Meta:
        verbose_name = 'Вопрос 3 типа'
        verbose_name_plural = 'Вопросы 3 типа'

    def __str__(self):
        return self.subject.name + " | " + self.text
