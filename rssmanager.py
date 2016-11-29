#!/usr/bin/env python
# -*- coding: utf-8 -*-
import PyRSS2Gen
import datetime
 
import re
import os
import magic
import mimetypes

from ConfigParser import ConfigParser

 
cp=ConfigParser()
 
class rssElaboraNuovi():
    def __init__(self,name='alboPretorio',title='',base_url='',description=''):
        self.name=name
	self.items = []
        self.title=title
        self.base_url=base_url
        self.description=description

    def do_rss(self,id_registro_num,id_registro_anno, tipo_atto, oggetto,link_dettaglio,data_inizio_pub,data_fine_pub):
	desc = '[%s/%s %s dal %s al %s] %s' % (str(id_registro_num), str(id_registro_anno), tipo_atto, data_inizio_pub, data_fine_pub, oggetto)
	dInizio = datetime.datetime.strptime(data_inizio_pub, '%d/%m/%Y')

	item = PyRSS2Gen.RSSItem (
		title=desc,
		guid=PyRSS2Gen.Guid(link_dettaglio),
		description = '',
		pubDate=dInizio)
	self.items.append(item)

    def out_rss(self,filename):
	rss = PyRSS2Gen.RSS2(
		title=self.title,
		link=self.base_url+'/'+filename,
		description=self.description,
		lastBuildDate=datetime.datetime.now(),
		items = self.items)
	rss.write_xml(open(filename,'w'))

    def __del__(self):
        pass


