from django.db import models

class Subject(models.Model):
    name = models.CharField('Название', max_length=20)
    subject_number = models.IntegerField('Номер')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'