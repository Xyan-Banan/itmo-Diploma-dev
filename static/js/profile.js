function remove(id, elem){
    name = document.getElementById(id).innerHTML;
    a = confirm('Вы действительно хотите удалить практику ' + name + '?');
    if (a){
        elem.setAttribute('name','remove');
        elem.setAttribute('value',id);
    }
}

function rename(id, elem){
    name = document.getElementById(id).innerHTML;
    newName = prompt('Введите новое имя для практики ' + name);
    if (newName){
        elem.setAttribute('name','rename');
        elem.setAttribute('value',id + '.' + newName);
    }
    else
        alert('Новое имя не может быть пустым');
}

function attach(id, elem){
    name = document.getElementById(id).innerHTML;
    group = elem.parentElement.children[1].selectedOptions[0].text;
    dateOfSub = elem.parentElement.children[2];
    console.log(dateOfSub);
    if (group == 'Группа' || group == 'Вы не ведете ни у одной группы'){
        alert('Ошибка в привязке группы.')
        return;
    }

    message = 'Привязать практику ' + name + ' к группе Y' + group;
    if (dateOfSub.validity.valid) {
        if(dateOfSub.value)
            message += ' со следующей датой сдачи:\n' + dateOfSub.value + '?';
        else
            message += '?';
    }
    else{
        alert('Ошибка при вводе даты сдачи практики.');
        return;
    }

    a = confirm(message);
    if (a){
        elem.setAttribute('name','attach');
        if (dateOfSub)
            elem.setAttribute('value',id + '.' + group + '.' + dateOfSub.value);
        else
            elem.setAttribute('value',id + '.' + group);
    }
}

function unattach(id, elem){
    name = document.getElementById(id).innerHTML;
    a = confirm('Вы действительно хотите отвязать практику ' + name + '?');
    if (a){
        elem.setAttribute('name','unattach');
        elem.setAttribute('value',id);
    }
}
