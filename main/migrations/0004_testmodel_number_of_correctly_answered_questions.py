# Generated by Django 4.1.7 on 2023-02-28 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_тема вопроса_questionstype1model_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testmodel',
            name='number_of_correctly_answered_questions',
            field=models.IntegerField(default=0, verbose_name='Количестов правильно отвеченных вопросов'),
        ),
    ]