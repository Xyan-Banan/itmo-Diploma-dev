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
    a = prompt('Введите новое имя для практики ' + name);
    if (a){
        elem.setAttribute('name','rename');
        elem.setAttribute('value',id + '.' + a);
    }
    else
        alert('Новое имя не может быть пустым');
}

function attach(id, elem){
    name = document.getElementById(id).innerHTML;
    group = elem.parentElement.children[1].selectedOptions[0].text;
    date_of_sub = elem.parentElement.children[2];
    console.log(date_of_sub);
    if (group == 'Группа' || group == 'Вы не ведете ни у одной группы'){
        alert('Ошибка в привязке группы.')
        return;
    }

    message = 'Привязать практику ' + name + ' к группе Y' + group;
    if (date_of_sub.validity.valid) {
        if(date_of_sub.value)
            message += ' со следующей датой сдачи:\n' + date_of_sub.value + '?';
        else
            message += '?';
    }
    else{
        alert('Ошибка при вводе даты сдачи практики.');
        return;
    }

    a = confirm(message);
    if (a){
        elem.setAttribute('name','rename');
        if (date_of_sub)
            elem.setAttribute('value',id + '.' + group + '.' + date_of_sub.value);
        else
            elem.setAttribute('value',id + '.' + group);
    }
}