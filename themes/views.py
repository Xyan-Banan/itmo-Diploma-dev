from django.shortcuts   import render
from django             import template
from django.http        import HttpResponse

def themes(request):     #request is object, that contains sessions, cookies, get, post and so on
    
    my_template = template.loader.get_template('themes.html')
    return HttpResponse(my_template.render())    #any view must return response type value


# Create your views here.
