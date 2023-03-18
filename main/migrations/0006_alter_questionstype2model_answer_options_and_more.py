# Generated by Django 4.1.7 on 2023-03-18 18:35

from django.db import migrations
import django_jsonform.models.fields
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_testmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionstype2model',
            name='answer_options',
            field=django_jsonform.models.fields.JSONField(help_text='Attention! Вырезайте изображения формул в примерно одинаковом масштабе!', verbose_name='Варианты ответов'),
        ),
        migrations.AlterField(
            model_name='questionstype3model',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(help_text='Attention! Для добавления формул при вырезании увеличивайте мастштаб! Изображения будут выводиться в том же масштабе, что вы и вырезали!', upload_to='img_for_type3/', verbose_name='Изображение для вопроса'),
        ),
        migrations.DeleteModel(
            name='QuestionsType4Model',
        ),
    ]
