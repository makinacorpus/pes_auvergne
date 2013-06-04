# -*- coding:utf-8 -*-
from django.db import models
from extended_choices import Choices
from coop.org.models import BaseOrganization

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

STATUTS = Choices(
    ('ASSO',    1,  'Association de loi 1901'),
    ('SCOP',    2,  'Société Coopérative Ouvrière de Production'),
    ('SCIC',    3,  'Société Coopérative d’Intérêt Collectif'),
    ('COOP47',  4,  'Société Coopérative de loi 1947'),
    ('EPCI',    5,  'Collectivité territoriale'),
)

class Organization(BaseOrganization):
    siret = models.CharField('Numero SIRET', blank=True, null=True, max_length=20)
    naf = models.CharField('Code d’activité NAF', blank=True, null=True, max_length=10)
    presage = models.CharField('Numero PRESAGE', blank=True, null=True, max_length=10)
    statut = models.PositiveSmallIntegerField('Statut juridique',
                                                choices=STATUTS.CHOICES,
                                                  default=STATUTS.ASSO)
    secteur_fse = models.PositiveSmallIntegerField('Secteur d’activité FSE',
                                                    choices=SECTEURS_FSE.CHOICES,
                                                    default=SECTEURS_FSE.TOUS)
    crowdfunding = models.URLField(u'crowdfunding', blank=True, null=True)

    class Meta:
        verbose_name = 'Initiative'
        verbose_name_plural = 'Initiatives'
        app_label = 'coop_local'

Organization._meta.get_field('category').verbose_name = u'catégorie ESS'
