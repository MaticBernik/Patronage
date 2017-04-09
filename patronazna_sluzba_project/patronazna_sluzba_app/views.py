from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import LoginForm

# Create your views here.
def index(request):

	# if this is a POST request we need to process the form data
    if request.method == 'POST':
            #return HttpResponseRedirect('/thanks/')
            return HttpResponse("Thanks, for trying.")
    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'index.html', {'login_form': form})

