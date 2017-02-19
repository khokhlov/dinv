#coding: utf-8
from __future__ import unicode_literals

from django.db import models

class Currency(models.Model):
    class Meta:
        verbose_name = u'Валюта'
        verbose_name_plural = u'Валюты'
        
    code = models.CharField(max_length = 1024,
                            verbose_name = u'Код',
                            help_text  = u'Код валюты, не более 1024-х символов')
    
    short_name = models.CharField(max_length = 1024,
                            verbose_name = u'Краткое название',
                            help_text  = u'Краткое название, не более 1024-х символов')
    
    name = models.CharField(max_length = 1024,
                            verbose_name = u'Название',
                            help_text  = u'Название, не более 1024-х символов')
    
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u'%s' % self.code


