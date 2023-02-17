from django.shortcuts import render

from main.forms import AddTestForm


def index(request):
    if request.method == 'POST':
        form = AddTestForm(request.POST)
        if form.is_valid():
            # Сюда логику
            pass
    else:
        form = AddTestForm()
    return render(request, 'main/index.html', {'form': form})
