#!/usr/bin/env python
# -*- coding: utf-8 -*-
from feedgen.feed import FeedGenerator
import datetime
import pytz
 
import re
import os
import magic
import mimetypes

from ConfigParser import ConfigParser

 
cp=ConfigParser()
 
class rssElaboraNuovi():
    def __init__(self,name='alboPretorio',title='',url='',description=''):
        self.name=name
	self.items = []
        self.title=title
        self.url=url
        self.description=description

    def do_rss(self,id_registro_num,id_registro_anno, tipo_atto, oggetto,link_dettaglio,data_inizio_pub,data_fine_pub):
	oggetto=oggetto
	desc = u'[%s/%s %s dal %s al %s] %s' % (str(id_registro_num), str(id_registro_anno), tipo_atto, data_inizio_pub, data_fine_pub, oggetto)
	dInizio = datetime.datetime.strptime(data_inizio_pub, '%d/%m/%Y')
	dInizio = pytz.timezone('EST').localize(dInizio)

	item = {
		'title':desc,
		'guid':link_dettaglio,
		'link':link_dettaglio,
		'tipo':tipo_atto,
		'description':desc,
		'pubDate':dInizio
	}
	print item
	self.items.append(item)

    def out_rss(self,filename):
	fg=FeedGenerator()
	fg.id(self.url)
	fg.title(self.title)
	fg.description(self.title)
	fg.author({'name':'alboPOP','email':''})
	fg.link(href=self.url)
	fg.language('it')

	for item in self.items:
		fe=fg.add_entry()
		fe.id(item['link'])
		fe.category(term=item['tipo'])
		fe.pubdate(item['pubDate'])
		fe.link(href=item['link'])
		fe.title(item['title'])
		fe.description(item['title'])

	fg.rss_file(filename)

    def __del__(self):
        pass


