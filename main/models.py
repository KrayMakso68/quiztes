from django.db import models

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