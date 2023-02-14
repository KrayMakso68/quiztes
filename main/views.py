from django.shortcuts import render
from main.forms import AddTestForm


# Create your views here.
def index(request):
    form = AddTestForm()
    data = {
        'form': form,
    }
    return render(request, 'main/index.html', data)
