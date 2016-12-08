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

from email.Utils import formatdate

from albopopExt import AlbopopExtension,AlbopopEntryExtension
 
cp=ConfigParser()
cp.read('alboPretorio.cfg')

RSS_TITLE=cp.get('rss', 'RSS_TITLE')
RSS_URL=cp.get('rss', 'RSS_URL')
RSS_DESC=cp.get('rss', 'RSS_DESC')
RSS_WEBMASTER=cp.get('rss', 'RSS_WEBMASTER')
 
class rssElaboraNuovi():
    def __init__(self,name='alboPretorio',title='',url='',description='',categoryType=None, categoryName=None):
        self.name=name
	self.items = []
        self.title=title
        self.url=url
        self.description=description
	self.categoryType=categoryType
	self.categoryName=categoryName

	self.webMaster=RSS_WEBMASTER

    def do_rss(self,id_registro_num,id_registro_anno, tipo_atto, oggetto,link_dettaglio,data_inizio_pub,data_fine_pub):
	oggetto=oggetto
	desc = u'[%s/%s %s dal %s al %s] %s' % (str(id_registro_num), str(id_registro_anno), tipo_atto, data_inizio_pub, data_fine_pub, oggetto)
	dInizio = datetime.datetime.strptime(data_inizio_pub, '%d/%m/%Y')
	dInizio = pytz.timezone('EST').localize(dInizio)

	item = {
		'title':oggetto,
		'guid':link_dettaglio,
		'link':link_dettaglio,
		'tipo':tipo_atto,
		'description':desc,
		'pubDate':dInizio,
		'numero':id_registro_num,
		'anno':id_registro_anno,
	}
	print item
	self.items.append(item)

    def out_rss(self,filename):
	fg=FeedGenerator()
	fg.register_extension('albopop',AlbopopExtension,AlbopopEntryExtension)
	fg.id(self.url)
	fg.title(self.title)
	fg.description(self.title)
	fg.author({'name':'alboPOP','email':''})
	fg.link(href=self.url)
	fg.pubDate(formatdate())
	fg.webMaster(self.webMaster)
	fg.docs('https://github.com/mfortini/alboPOP_saga')
	fg.language('it')

	fg.albopop.categoryName(self.categoryName)
	fg.albopop.categoryType(self.categoryType)

	for item in self.items:
		fe=fg.add_entry()
		fe.id(item['link'])
		fe.category(term=item['tipo'])
		fe.pubdate(item['pubDate'])
		fe.link(href=item['link'])
		fe.title(item['title'])
		fe.description(item['description'])
		fe.albopop.categoryUID(str(item['numero'])+'/'+str(item['anno']))

	fg.rss_file(filename)

    def __del__(self):
        pass


