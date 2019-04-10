from django             import template
from django.http        import HttpResponse

def themes(request):     #request is object, that contains sessions, cookies, get, post and so on
    
    my_template = template.loader.get_template('themes.html')
    return HttpResponse(my_template.render())    #any view must return response type value

def login(request):

    my_template = template.loader.get_template('login.html')
    return HttpResponse(my_template.render())

def profile(request):

    my_template = template.loader.get_template('profile.html')

    class Profile:
        name = ''
        sername = ''
        patronymic = ''
        status = ''

        def __init__(self, name,sername,patronymic,status):
            self.name = name
            self.sername = sername
            self.patronymic = patronymic
            self.status = status

    my_profile = Profile ('John','Romero','','student')

    c = template.Context({'profile':my_profile})

    return HttpResponse(my_template.render({'profile':my_profile}))

# Create your views here.
