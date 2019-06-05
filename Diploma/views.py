from pathlib import Path
import random
import os

from django.shortcuts           import render,redirect
from django.core.exceptions     import ObjectDoesNotExist, PermissionDenied
from django.contrib.staticfiles import finders

import bcrypt

from Diploma.models             import User, Theme, Group, Practice

def index(request):
    if 'user' in request.session:
        return redirect('Diploma:profile')
    return redirect('Diploma:login')


def login(request):

    if 'user' in request.session:
        return redirect('Diploma:profile')

    # check for method then check other things
    if request.method == 'POST':
        login_string = request.POST.get('login')
        password = request.POST.get('password')
        # check for empty login or password
        if login_string and password:
            # check if exist user with login
            try:
                user = User.objects.get(login = login_string)
            except ObjectDoesNotExist:
                return render(request, 'login.html',{'message':'Логин или пароль не существуют'})
            
            hashedpw = bcrypt.hashpw(password.encode(),user.password.encode())
            # check hashed password for user
            if  hashedpw == user.password.encode():
                request.session['user'] = user
                request.session.set_expiry(0)
                # check if need to redirect straight to another page
                if next in request.POST:
                    return redirect(request.POST[next])
                else:
                    return redirect('Diploma:profile',)
            else:    
                return render(request, 'login.html',{'message':'Логин или пароль не существуют'})
        else:
            return render(request, 'login.html',{'message':'Логин или пароль не введен'})
        
    return render(request, 'login.html')

def profile(request):

    if 'user' not in request.session:
        return redirect('Diploma:login')

    if 'logout' in request.POST:
        del request.session['user']
        return redirect('Diploma:profile')

    user = request.session['user']
    groups_list = Group.objects.filter(teacher=user.id_user).order_by('number')

    context = {
        'profile':user,
        'groups_list':groups_list
        }
    return render(request, 'profile.html', context)

def createthemelist(request):
    
    themes_list = {}
    
    for key,value in request.POST.items():
        # add themes into the list
        if key[:5] == 'theme':
            # trying to conver value to task quantity
            try:
                value = int(value)
            except ValueError:
                # if string is empry - initiate by 0
                if value == '':
                    value = 0
                else:
                    return -1
            # if task quantity is negative number - then return error value
            if value < 0:
                return -1
            # if task quantity is 0 then pass this theme
            elif value == 0:
                continue
            themes_list[key[5:]] = value
    # if theme_list i empty - send error value
    if not themes_list:
        return -1
    return themes_list

def InitTaskArray(dir_path):
    a = []

    files = dir_path.iterdir()
    for i in files:
        file_path = dir_path.joinpath(i.name)
        task_file = file_path.open('r')
        a.append(task_file.read())
    return a

def InitTasksInThemes(themes_list):
    tasks_in_themes = {}
    
    for id_theme in themes_list.keys():
        theme = Theme.objects.get(pk=id_theme)
        theme_abs_path = Path(finders.find(theme.path))
        tasks_array = InitTaskArray(theme_abs_path)
        tasks_in_themes[id_theme] = tasks_array
    
    return tasks_in_themes

def createfile(request):

    themes_list = createthemelist(request)
    if themes_list == -1:
        return -1

    practice_name = request.POST['practice_name']
    # practice = Practice(name=practice_name,path='practics/')
    prac_dir_abs_path = Path(finders.find('practics/'))
    tmp_prac_abs_path = prac_dir_abs_path.joinpath('tmp_' + practice_name + '.tex')
    tmp_practice = tmp_prac_abs_path.open('w+')
    tmp_practice.write('\\documentclass{article}\n')
    tmp_practice.write('\\usepackage[utf8]{inputenc}\n')
    tmp_practice.write('\\usepackage[russian]{babel}\n\n')
    tmp_practice.write('\\begin{document}\n\n')
    variants_quant = int(request.POST['variants_quantity'])
    
    tasks_in_themes = InitTasksInThemes(themes_list)
    
    # cycle by variants
    for i in range(variants_quant):
        tmp_practice.write('\n\\centering {Вариант ' + str(i + 1) + '}\n\n')
        # cycle by themes
        for id_theme in themes_list.keys():
            tmp_practice.write('\\begin{itemize}\n')
            for j in range(int(themes_list[id_theme])):
                selected_task = tasks_in_themes[id_theme].pop(random.randint(0, len(tasks_in_themes[id_theme]) - 1))
                tmp_practice.write(selected_task)
            tmp_practice.write('\\end{itemize}\n\n')
    
    tmp_practice.write('\\end{document}\n')
    tmp_practice.close()

    os.chdir(prac_dir_abs_path)
    os.system('pdflatex ' + str(tmp_prac_abs_path)[:-4])


    return 0 #practice.id

def checkformthemes(request):
    
    try:
        Practice.objects.get(name=request.POST['practice_name'])
    except ObjectDoesNotExist:
        if ('practice_name' in request.POST) and (request.POST['practice_name'] != ''):
            # check if variants quantity exist and more then zero
            if ('variants_quantity' in request.POST) and (request.POST['variants_quantity'] != ''):
                if int(request.POST['variants_quantity']) > 0:
                    return 1
                else:
                    context = {'message':'Не введено или введено неверно количество вариантов'}
            else:
                context = {'message':'Не введено или введено неверно количество вариантов'}
        else:
            context = {'message':'Не введено название практики'}
        return context
    return {'message':'Практика с таким именем уже существует'}

def create_practice(request):

    if 'user' not in request.session:
        return redirect('Diploma:login')
    
    if request.session['user'].status != 'teacher':
        raise PermissionDenied
    
    themes_list = Theme.objects.order_by('name')

    context = {
        'themes_list':themes_list
    }

    # check for clicked submit button
    if 'submit' in request.POST:
        check = checkformthemes(request)
        if check != 1:
            context['message'] = check['message']
        else:
            practice_id = createfile(request)
            if practice_id == -1:
                context['message'] ='Не выбрано ни одной темы или неверно введено количество заданий'
    
    return render(request, 'create_practice.html',context)