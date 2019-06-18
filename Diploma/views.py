from pathlib import Path
import random
import os

from django.http                import HttpResponseNotFound
from django.shortcuts           import render,redirect
from django.core.exceptions     import ObjectDoesNotExist, PermissionDenied
from django.contrib.staticfiles import finders

import bcrypt

from Diploma.models             import User, Theme, Group, Practice, PracticeForGroup

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

    # if 'remove' in request.POST:
    #     continue

    user = request.session['user']
    context = {
        'profile':user,
        }
    if user.status == 'teacher':
        groups_list = Group.objects.filter(teacher=user.id_user).order_by('number')
        practice_list = Practice.objects.all()
        practice_for_groups_list = PracticeForGroup.objects.values_list('id_practice',flat=True)
        for practice in practice_list:
            practice.name = practice.name.replace('_',' ')
            if practice.id_practice in practice_for_groups_list:
                practice_list.remove(practice)
        context['groups_list'] = groups_list
        context['practice_list'] = practice_list
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
    "returns array of file names in dir_path"
    a = []

    files = dir_path.iterdir()
    for i in files:
        a.append(i.name)
    return a

def InitTasksInThemes(themes_list):
    "returns dict of filenames in each theme"
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
    practice_name = practice_name.replace(' ','_')
    prac_dir_abs_path = Path(finders.find('practics/'))
    tmp_prac_abs_path = prac_dir_abs_path.joinpath('tmp_' + practice_name + '.tex')
    tmp_practice = tmp_prac_abs_path.open('w+')
    tmp_practice.write('''  \\documentclass{article}\n
                            \\usepackage[utf8]{inputenc}\n
                            \\usepackage[russian]{babel}\n\n
                            \\begin{document}\n\n''')
    variants_quant = int(request.POST['variants_quantity'])
    
    tasks_in_themes = InitTasksInThemes(themes_list)
    selected_tasks = {}
    # cycle by variants
    for i in range(variants_quant):
        tmp_practice.write('\n\\centering {Вариант ' + str(i + 1) + '}\n\n')
        selected_tasks[i] = {}
        # cycle by themes
        for id_theme in themes_list.keys():
            selected_tasks[i][id_theme] = []
            tmp_practice.write('\\begin{itemize}\n')
            number_of_needed_tasks = int(themes_list[id_theme])
            theme = Theme.objects.get(pk=id_theme)
            theme_abs_path = Path(finders.find(theme.path))
            # cycle by needed number of tasks
            for j in range(number_of_needed_tasks):
                # check if need to refill tasks_in_theme array with tasks
                tasks_quantity = len(tasks_in_themes[id_theme])
                if tasks_quantity - 1 < number_of_needed_tasks - j:
                    tasks_in_themes[id_theme] = InitTaskArray(theme_abs_path)
                    tasks_quantity = len(tasks_in_themes[id_theme])
                # get random task
                task_num = random.randint(0, tasks_quantity - 1)
                # get task's file name, path, open task's file and write it to .tex tmp file
                task_name = tasks_in_themes[id_theme].pop(task_num)
                task_path = theme_abs_path.joinpath(task_name)
                with task_path.open('r') as selected_task:
                    tmp_practice.write(selected_task.read())
                selected_tasks[i][id_theme].append(task_name)
            tmp_practice.write('\\end{itemize}\n\n')

    tmp_practice.write('\\end{document}\n')
    tmp_practice.close()

    os.chdir(prac_dir_abs_path)
    os.system('pdflatex ' + str(tmp_prac_abs_path)[:-4])

    tmp_prac_abs_path = Path(tmp_prac_abs_path.cwd()).joinpath('tmp_' + practice_name + '.pdf')
    tmp_prac_abs_path.rename(practice_name + '.pdf')
    print('-----------------' + str(tmp_prac_abs_path.cwd()) + '------------')
    for i in prac_dir_abs_path.iterdir():
        if i.name[:3] == 'tmp':
            del_path = prac_dir_abs_path.joinpath(i.name)
            del_path.unlink()

    practice = Practice(name=practice_name,path='practice/')
    practice.save()

    return practice.id_practice

def checkformthemes(request):
    
    if ('practice_name' not in request.POST) or (request.POST['practice_name'] == '') or (request.POST['practice_name'][:3] == 'tmp'):
        return {'message':'Не введено или неверно введено название практики'}

    practice_name = request.POST['practice_name']
    practice_name = practice_name.replace(' ','_')

    try:
        Practice.objects.get(name=practice_name)
    except ObjectDoesNotExist:
        # check if variants quantity exist and more then zero
        if ('variants_quantity' in request.POST) and (request.POST['variants_quantity'] != ''):
            if int(request.POST['variants_quantity']) > 0:
                return 1
            else:
                context = {'message':'Не введено или введено неверно количество вариантов'}
        else:
            context = {'message':'Не введено или введено неверно количество вариантов'}
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
            else:
                redirect('Diploma:show_practice',practice_id=practice_id)
    
    return render(request, 'create_practice.html',context)

def show_practice(request, practice_id):
    
    if 'user' not in request.session:
        return redirect('Diploma:login')

    try:
        practice = Practice.objects.get(pk=practice_id)
        context = {
            'practice_name':practice.name + '.pdf'
        }
        
        return render(request, 'show_practice.html',context)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    