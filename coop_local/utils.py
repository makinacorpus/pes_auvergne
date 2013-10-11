# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives
from django.utils import simplejson

def mail_to_friend(request):
    
    if request.method == "GET" :
        
        dest = request.GET['dest']
        url = request.GET['url']

        plaintext = get_template('utils/send_mail_link.txt')

        d = Context({ 'url': url})

        text_content = plaintext.render(d)

        title = _("Link to PES Auvergne")
        sender = "contact@echanges-solidaires-auvergne.fr"
        msg = EmailMultiAlternatives(title, text_content, sender, [dest])

        try:
            res = msg.send()
            response_text = _('Link sent, thank you')
        except:   
            response_text = _('An error has occured. Please try again or contact an administrator')
    
    to_json = {
        "msg": response_text,
    }
    return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')    
    
    


    




