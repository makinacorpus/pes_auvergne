# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.utils.translation import ugettext as _
from django.core.mail import EmailMultiAlternatives
from django.utils import simplejson
from django.conf import settings

from coop_local.models import Person, Engagement

def mail_to_friend(request):
    
    if request.method == "GET" :
        
        dest = request.GET['dest']
        url = request.GET['url']

        plaintext = get_template('utils/send_mail_link.txt')

        d = Context({ 'url': url})

        text_content = plaintext.render(d)

        title = _("Link to PES Auvergne")
        sender = settings.MAIN_EMAIL

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
    
    
def notify_object_creation(url):
    
    plaintext = get_template('utils/send_mail_moderation.txt')

    d = Context({ 'url': url})

    text_content = plaintext.render(d)

    title = _("PES Auvergne - Notification")
    sender = settings.MAILING_MODERATION
    dest = settings.MAILING_MODERATION
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
    

def user_linked_to_organization(user):
    # Check if user is connected to an organization

    if user.is_superuser:
        return True
    else:
        try:
            pes_user = Person.objects.get(user=user)
        except Person.DoesNotExist:
            pes_user = None

        if pes_user :
            engagement = Engagement.objects.filter(person=pes_user)
            if engagement:
                return True
                
    return False
    
    

    




