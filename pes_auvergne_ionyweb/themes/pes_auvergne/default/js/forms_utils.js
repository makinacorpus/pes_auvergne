function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
}
    
    
function textCounter( field, maxLimit) {
    if ( field.value.length > maxLimit )
    {
        field.value = field.value.substring( 0, maxLimit );
        return false;
    }
}


function delete_object(msg, url) {
    if(confirm(msg)) {
        $(location).attr('href',url)
    }
}


function send_to_friend(url, id_mail, id_infos) {
    mail = document.getElementById(id_mail).value;
    infos_obj = document.getElementById(id_infos);
    if(!mail) {
        alert(gettext("You have to write a destination mail"));
        return;
    }
    
    url = "/mailto/?url=" + url + "&dest=" + mail;
    var jqxhr = $.ajax(url)
        .done(function(response) {
            infos_obj.innerHTML = response.msg;
        })
        .fail(function(response) {
            infos_obj.innerHTML = response.msg;
        });
}

function open_popup_link(id) {
    $(function() {
        $( id ).dialog({
            height: 200,
            modal: true
        });
    });
}
