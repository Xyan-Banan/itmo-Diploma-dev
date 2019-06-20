from pathlib import Path
import random
import os
import datetime

from django.http                import HttpResponseNotFound
from django.shortcuts           import render,redirect
from django.core.exceptions     import ObjectDoesNotExist, PermissionDenied
from django.contrib.staticfiles import finders

import bcrypt

from Diploma.models             import User, Theme, Group, Practice, PracticeForGroup, Material

def index(request):
    if 'user' in request.session:
        return redirect('Diploma:profile')
    return redirect('Diploma:login')

def login(request):

    if 'user' in request.session:
        return redirect('Diploma:profile')

    material_list = Material.objects.all().order_by('name')
    context = {
        'material_list':material_list
    }

    # check for method then check other things
    if request.method == 'POST':
        login_string = request.POST.get('login')
        password = request.POST.get('password')
        # check for empty login or password
        if login_string and password:
            # check if exist user with login
            try:
                user = User.objects.get(login__regex=login_string)
            except ObjectDoesNotExist:
                context ['message'] = 'Логин или пароль не существуют'
                return render(request, 'login.html',context)
            
            hashedpw = bcrypt.hashpw(password.encode(),user.password.encode())
            # check hashed password for user
            if  hashedpw == user.password.encode():
                request.session['user'] = user
                request.session.set_expiry(0)
                return redirect('Diploma:profile',)
            else:
                context ['message'] = 'Логин или пароль не существуют'
                return render(request, 'login.html',context)
        else:
            context ['message'] = 'Логин или пароль не введен'
            return render(request, 'login.html',context)
        
    return render(request, 'login.html', context)

def check_practice_action(request):
    if 'rename' in request.POST:
        id_practice, new_name = request.POST['rename'].split('.')
        try:
            check_practice = Practice.objects.get(name__regex=new_name)
            print(check_practice)
            return 'Практика с таким именем уже существует'
        except ObjectDoesNotExist:
            try:
                practice = Practice.objects.get(pk=id_practice)
                practice.name = new_name
                practice.save()
                return
            except ObjectDoesNotExist as ex:
                print(format(ex))
                return 'Ошибка переименования практики'

    if 'remove' in request.POST:
        id_practice = request.POST['remove']
        try: 
            Practice.objects.get(pk=id_practice).delete()
            return
        except ObjectDoesNotExist as ex:
            print(format(ex))
            return 'Ошибка удаления практики'
    
    if 'attach' in request.POST:
        attach = request.POST['attach'].split('.')
        try:
            practice = Practice.objects.get(pk=attach[0])
            group = Group.objects.get(number=attach[1])
            date_of_sub = attach[2] if len(attach) > 2 else ''
            if date_of_sub:
                pr_for_gr = PracticeForGroup(id_practice=practice,id_group=group,date_of_sub=date_of_sub)
            else:
                pr_for_gr = PracticeForGroup(id_practice=practice,id_group=group)
            pr_for_gr.save()
            return
        except ObjectDoesNotExist as ex:
            print(format(ex))
            return 'Ошибка привязки группы'
    
    if 'unattach' in request.POST:
        unattach = request.POST['unattach']
        try:
            PracticeForGroup.objects.get(pk=unattach).delete()
            return
        except ObjectDoesNotExist as ex:
            print(format(ex))
            return 'Ошибка отвязки практики'

def fill_teachers_interface(request): 
    user = request.session['user']
    groups_list = Group.objects.filter(teacher=user.id_user).order_by('number')
    # check and perform database changes
    alert_message = check_practice_action(request)
    # get all practices and list of connections practices with group
    practice_for_groups_list = PracticeForGroup.objects.all()
    print(practice_for_groups_list)
    attached_practices = dict(practice_for_groups_list.values_list('id_practice','date_of_sub'))
    for i in attached_practices:
        if attached_practices[i] is not None:
            attached_practices[i] = attached_practices[i].strftime('%d.%m.%Y')
        else:
            attached_practices[i] = ''
    print(attached_practices)
    print(attached_practices.items())
    practice_list = Practice.objects.all().order_by('name')
    if 'get_practices' in request.GET:
        group_num = request.GET['get_practices']
        # check, which practices needed to be shown
        if group_num == 'Все':
            group_num = 'Все практики'
        elif group_num != 'Непривязанные' and group_num != 'Вы не ведете ни у одной группы':
            id_group = Group.objects.get(number=group_num).id_group
            practice_for_groups_list = practice_for_groups_list.filter(id_group=id_group).values_list('id_practice',flat=True)
            practice_list = practice_list.filter(id_practice__in=practice_for_groups_list)
            group_num = 'Практики группы Y' + group_num
        else:
            practice_for_groups_list = practice_for_groups_list.values_list('id_practice',flat=True)
            practice_list = practice_list.exclude(id_practice__in=practice_for_groups_list)
            group_num = 'Непривязанные практики'
    else:
        group_num = 'Все практики'

    practice_list = dict(practice_list.values_list('id_practice','name'))
    practice_list = {i:practice_list[i].replace('_',' ') for i in practice_list}
    print(practice_list)
    # setting minimum date to submit the practice
    now = str(datetime.datetime.now() + datetime.timedelta(days=1))[:10]
    context = {
        'profile':user,
        'group_attachment':group_num,
        'groups_list':groups_list,
        'practice_list':practice_list,
        'attached_practices':attached_practices,
        'today':now
    }
    if alert_message:
        context['alert_message'] = alert_message
    return render(request, 'profile_teacher.html', context)

def fill_students_interface(request):
    user = request.session['user']

    connections = dict(PracticeForGroup.objects.filter(id_group=user.group).order_by('date_of_sub').values_list('id_practice','date_of_sub'))
    print (connections)
    for conn in connections:
        if connections[conn] is not None:
            connections[conn] = connections[conn].strftime('%d.%m.%Y') 
        else:
            connections[conn] = ''
    
    attached_practices = dict(Practice.objects.filter(id_practice__in=connections).values_list('id_practice','name'))
    for i in attached_practices:
        attached_practices[i] = {'name':attached_practices[i].replace('_',' '),'date_of_sub':connections[i]}

    print(attached_practices)

    material_list = Material.objects.all().order_by('name')

    context = {
        'profile':user,
        'attached_practices':attached_practices,
        'material_list':material_list
        }

    return render(request,'profile_student.html',context)

def profile(request):
    if 'user' not in request.session:
        return redirect('Diploma:login')

    if 'logout' in request.POST:
        del request.session['user']
        return redirect('Diploma:profile')

    user = request.session['user']
    
    if user.status == 'teacher':
        return fill_teachers_interface(request)
    
    return fill_students_interface(request)

def init_task_array(dir_path):
    "returns array of file names in dir_path"
    task_array = []

    files = dir_path.iterdir()
    for i in files:
        task_array.append(i.name)
    return task_array

def init_tasks_in_themes(themes_list):
    "returns dict of filenames in each theme"
    tasks_in_themes = {}
    
    for id_theme in themes_list.keys():
        theme = Theme.objects.get(pk=id_theme)
        theme_abs_path = Path(finders.find(theme.path))
        tasks_array = init_task_array(theme_abs_path)
        tasks_in_themes[id_theme] = tasks_array
    
    return tasks_in_themes

def create_theme_list(post):
    
    themes_list = {}
    
    for key,value in post.items():
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

def create_file(post):

    themes_list = create_theme_list(post)
    if themes_list == -1:
        return -1

    practice_name = post['practice_name']
    practice_name = practice_name.replace(' ','_')
    prac_dir_abs_path = Path(finders.find('practics/'))
    tmp_prac_abs_path = prac_dir_abs_path.joinpath('tmp_' + practice_name + '.tex')
    tmp_practice = tmp_prac_abs_path.open('w+')
    tmp_practice.write('''  \\documentclass{article}\n
                            \\usepackage[utf8]{inputenc}\n
                            \\usepackage[russian]{babel}\n\n
                            \\begin{document}\n\n''')
    variants_quant = int(post['variants_quantity'])
    
    tasks_in_themes = init_tasks_in_themes(themes_list)
    selected_tasks = {}
    # cycle by variants
    for i in range(variants_quant):
        tmp_practice.write('\n\\centering {Вариант ' + str(i + 1) + '}\n\n')
        selected_tasks[i] = {}
        # cycle by themes
        for id_theme in themes_list:
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
                    tasks_in_themes[id_theme] = init_task_array(theme_abs_path)
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

    practice = Practice(name=practice_name,path='practics/')
    practice.save()

    return practice.id_practice

def check_form_themes(post):
    
    if ('practice_name' not in post) or (post['practice_name'] == '') or (post['practice_name'][:3] == 'tmp'):
        return {'message':'Не введено или неверно введено название практики'}

    practice_name = post['practice_name']
    practice_name = practice_name.replace(' ','_')

    try:
        Practice.objects.get(name=practice_name)
    except ObjectDoesNotExist:
        # check if variants quantity exist and more then zero
        if ('variants_quantity' in post) and (post['variants_quantity'] != ''):
            if int(post['variants_quantity']) > 0:
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

    post = request.POST

    # check for clicked submit button
    if 'submit' in post:
        check = check_form_themes(post)
        if check != 1:
            context['message'] = check['message']
        else:
            practice_id = create_file(post)
            if practice_id == -1:
                context['message'] ='Не выбрано ни одной темы или неверно введено количество заданий'
            else:
                request.session['post'] = request.POST
                return redirect('/profile/show_practice/' + str(practice_id) + '?from_create=true')
    
    return render(request, 'create_practice.html',context)

def check_show_action(request, id_practice):
    if 'save' in request.POST:
        del request.session['post']
        return 'profile'
    
    if 'cancel' in request.POST:
        if 'from_create' in request.GET:
            Practice.objects.get(pk=id_practice).delete()
            del request.session['post']
        return 'profile'

    if 'regen' in request.POST:
        Practice.objects.get(pk=id_practice).delete()
        if request.POST['regen'] == 'this_param':
            new_id = create_file(request.session['post'])
            return new_id
        else:
            del request.session['post']
            return 'create_practice'

    if 'attach' in request.POST:
        attach = request.POST['attach'].split('.')
        try:
            practice = Practice.objects.get(pk=id_practice)
            group = Group.objects.get(number=attach[0])
            date_of_sub = attach[1] if len(attach) > 1 else ''
            if date_of_sub:
                pr_for_gr = PracticeForGroup(id_practice=practice,id_group=group,date_of_sub=date_of_sub)
            else:
                pr_for_gr = PracticeForGroup(id_practice=practice,id_group=group)
            pr_for_gr.save()
            return 'profile'
        except ObjectDoesNotExist as ex:
            print(format(ex))
            return 'Ошибка привязки группы'

def show_practice(request, id_practice):
    
    if 'user' not in request.session:
        return redirect('Diploma:login')

    user = request.session['user']
    if (user.status != 'teacher') and ('from_create' in request.GET):
        raise PermissionDenied
    
    check = check_show_action(request, id_practice)
    if check == 'profile':
        return redirect('Diploma:profile')
    elif check == 'create_practice':
        return redirect('Diploma:create_practice')

    try:
        practice = Practice.objects.get(pk=id_practice)
        groups_list = Group.objects.filter(teacher=user.id_user).order_by('number')
        now = str(datetime.datetime.now() + datetime.timedelta(days=1))[:10]
        
        context = {
            'practice_name':practice.name + '.pdf',
            'group_list':groups_list,
            'today':now
        }
        
        return render(request, 'show_practice.html',context)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    
def show_material(request,id_material):
    try:
        material = Material.objects.get(pk=id_material)
        material = material.name + '.pdf'
        context = {
            'material_name':material
        }
        print (context)
        return render(request,'show_material.html', context)
    except ObjectDoesNotExist as ex:
        print(ex);
        return HttpResponseNotFound
