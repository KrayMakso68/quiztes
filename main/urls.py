from os import name

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("test/<int:question_number>", views.viewquestion, name='viewquestion'),
    path("test/results", views.viewresults, name='view-results'),
]