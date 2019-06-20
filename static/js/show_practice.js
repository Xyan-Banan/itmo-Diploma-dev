function attach(name, elem){
    group = document.getElementById('group').selectedOptions[0].text;
    dateOfSub = document.getElementById('date_of_sub');
    console.log(dateOfSub);
    if (group == 'Группа'){
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
            elem.setAttribute('value',group + '.' + dateOfSub.value);
        else
            elem.setAttribute('value',group);
    }
}