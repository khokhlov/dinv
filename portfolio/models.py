#coding: utf-8
from __future__ import unicode_literals

from django.db import models

class Portfolio(models.Model):
    class Meta:
        verbose_name = u'Инвестиционный портфель'
        verbose_name_plural = u'Инвестиционные портфели'
        
    name = models.CharField(max_length = 1024,
                            verbose_name = u'Портфель',
                            help_text  = u'Название портфеля, не более 1024 символа')
    
    created_date = models.DateTimeField(auto_now_add = True)
    
    modified_date = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return u'%s' % self.name
