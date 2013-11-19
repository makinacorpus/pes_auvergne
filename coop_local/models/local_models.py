# -*- coding:utf-8 -*-
from django.db import models
from extended_choices import Choices
from coop.org.models import BaseOrganization
from django.utils.translation import ugettext_lazy as _

SECTEURS_FSE = Choices(
    ('TOUS',        0,  'Tous secteurs d’activité'),
    ('EQUITABLE',   1,  'Commerce équitable de biens et services'),
    ('OFFLINE',     2,  'Culture, loisirs, sport'),
    ('TOURISME',    3,  'Eco-tourisme'),
    ('ENV',         4,  'Environnement, énergies renouvelable'),
    ('TIC',         5,  'Information et Communication'),
    ('TRANSPORT',   6,  'Transport,mobilité'),
    ('SERVICE',     7,  'Services aux personnes'),
    ('AUTRE',       8,  'Autres activités')
)

EVALUATE_ANSWERS = Choices(
    ('NONE', 0, _(u'None')),
    ('INTERESTED', 1, _(u'No action but interest')),
    ('REGULAR', 3, _('Regular actions')),
    ('SPECIALIST', 4, _('Specialist')),
)
    
class EvaluationQuestionTheme(models.Model):
    label = models.CharField(blank=True, max_length=1024)
    cssclass = models.CharField(blank=True, max_length=50)
    class Meta:
        verbose_name = _(u'evaluate theme')
        verbose_name_plural = _(u'evaluate theme')
        ordering = ['label']
        app_label = 'coop_local'

    def __unicode__(self):
        return self.label

class Evaluation(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        verbose_name = _(u'evaluate')
        verbose_name_plural = _(u'evaluate')
        app_label = 'coop_local'

class EvaluationQuestion(models.Model):
    label = models.CharField(blank=True, max_length=512)
    question = models.CharField(max_length=512)
    theme = models.ForeignKey(EvaluationQuestionTheme,blank=True, null=True)

    class Meta:
        verbose_name = _(u'evaluation question')
        verbose_name_plural = _(u'evaluation question')
        app_label = 'coop_local'

    def __unicode__(self):
        return self.question


class EvaluationAnswer(models.Model):
    evaluation = models.ForeignKey(Evaluation)
    question = models.ForeignKey(EvaluationQuestion)
    answer = models.SmallIntegerField(verbose_name=_(u'answer'),choices=EVALUATE_ANSWERS, blank=True, null=True)
    experience = models.TextField(verbose_name=_(u'experiences'),blank=True, null=True)

    class Meta:
        verbose_name = _(u'evaluation answer')
        verbose_name_plural = _(u'evaluation answer')
        app_label = 'coop_local'

    def __unicode__(self):
        return self.answer


class Organization(BaseOrganization):
    siret = models.CharField('Numero SIRET', blank=True, null=True, max_length=20)
    naf = models.CharField('Code d’activité NAF', blank=True, null=True, max_length=10)
    presage = models.CharField('Numero PRESAGE', blank=True, null=True, max_length=10)
    secteur_fse = models.PositiveSmallIntegerField('Secteur d’activité FSE',
                                                    choices=SECTEURS_FSE.CHOICES,
                                                    default=SECTEURS_FSE.TOUS)
    crowdfunding = models.URLField(u'crowdfunding', blank=True, null=True)
    description2 = models.TextField(u'en savoir plus', blank=True, null=True)

    evaluation = models.ForeignKey('coop_local.Evaluation', verbose_name=_(u'answer'), blank=True, null=True)
    
    evaluation_status = models.BooleanField(_('Publish evaluation'), default=False)
    
    class Meta:
        verbose_name = 'Initiative'
        verbose_name_plural = 'Initiatives'
        app_label = 'coop_local'

Organization._meta.get_field('category').verbose_name = u'catégorie ESS'
Organization._meta.get_field('description').verbose_name = u'présentation générale'
