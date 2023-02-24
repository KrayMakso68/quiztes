from django.contrib import admin
from main.models import Subject, QuestionsType1Model, QuestionsType2Model


class ID_Admin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Subject)
admin.site.register(QuestionsType1Model, ID_Admin)
admin.site.register(QuestionsType2Model, ID_Admin)
