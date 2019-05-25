from django.shortcuts   import render

def themes(request):     #request is object, that contains sessions, cookies, get, post and so on
    # here need to get all themes from DB and put their names in array
    # then send this array as context to template
    return render(request,'themes.html')    #any view must return response type value; the render shortcut returns response

def login(request):
    return render(request,'login.html')

def profile(request):

    

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

    my_profile = Profile ('John','Romero','Иванович','teacher')
    context = {'profile':my_profile}
    
    return render(request,'profile.html',context)

