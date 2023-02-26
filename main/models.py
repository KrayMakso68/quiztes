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
    questions = models.JSONField('Вопросы теста')

    def __str__(self):
        return self.surname_name


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
        return self.text


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
    answer_options = JSONField('Варианты ответов', schema=ITEMS_SCHEMA, file_handler='main/static/main/uploaded_img/')
    right_answer = models.IntegerField('Номер верного ответа (по порядку)')

    class Meta:
        verbose_name = 'Вопрос 2 типа'
        verbose_name_plural = 'Вопросы 2 типа'


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
    image = models.ImageField('Изображение для вопроса', upload_to='main/static/main/uploaded_img')
    answer_options = JSONField('Варианты ответов', schema=ITEMS_SCHEMA)
    right_answer = models.IntegerField('Номер верного ответа (по порядку)')

    class Meta:
        verbose_name = 'Вопрос 3 типа'
        verbose_name_plural = 'Вопросы 3 типа'


class QuestionsType4Model(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.SET_NULL, null=True)
    text = models.TextField('Текст вопроса')
    right_answer = models.DecimalField("Числовой ответ (разделитель ' , ')", decimal_places=5, max_digits=5)

    class Meta:
        verbose_name = 'Вопрос 4 типа'
        verbose_name_plural = 'Вопросы 4 типа'
# для загрузки файлов
# file_handler='main/static/main/uploaded_img'
