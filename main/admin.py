from django.contrib import admin
from main.models import Subject, QuestionsType1Model, QuestionsType2Model, QuestionsType3Model, TestModel


class ID_Admin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Subject)
admin.site.register(QuestionsType1Model, ID_Admin)
admin.site.register(QuestionsType2Model, ID_Admin)
admin.site.register(QuestionsType3Model, ID_Admin)
admin.site.register(TestModel, ID_Admin)
