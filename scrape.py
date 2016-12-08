#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
import requests
import re
import rssmanager as RSS
import time
import sys

from ConfigParser import ConfigParser


cp=ConfigParser()
cp.read('alboPretorio.cfg')

BASE_OUT_URL=cp.get('settings', 'ALBO_BASE_URL')
DIRNAME=cp.get('settings', 'FILES_BASE_PATH')

SAGA_BASE="http://pubblicazioni.saga.it"
SAGA_ORGS=SAGA_BASE+"/orgs/"

if len(BASE_OUT_URL) == 0 or len(DIRNAME) == 0:
	print "ERROR SETTINGS"
	sys.exit(1)

def outputRSS(alboName,data,dirName):
    rssName="alboPOP - Comune - " + alboName.title()
    rssTitle="*non ufficiale* RSS feed dell'Albo Pretorio del Comune di " + alboName.title()
    rss=RSS.rssElaboraNuovi(name=rssName,title=rssTitle,url=BASE_OUT_URL+"/alboPOP"+alboName+".xml")
    for row in data:
        nReg=row[0]
        dataReg=row[1]
        nAtto=row[2]
        tipo=row[3]
        oggetto=re.sub(r'\s*/g',' ',row[4])
        inizioPub,finePub=row[6].split('-')
        inizioPub=re.sub(r'(\d*)\/(\d*)\/(\d*)',r'\1/\2/20\3',inizioPub.strip())
        finePub=re.sub(r'(\d*)\/(\d*)\/(\d*)',r'\1/\2/20\3',finePub.strip())
        link=row[7].strip()

        rss.do_rss(nReg,dataReg, tipo, oggetto,link,inizioPub,finePub)
    outputFileName=dirName+'/'+'alboPOP'+alboName+'.xml'
    print "writing to",outputFileName
    rss.out_rss(outputFileName)

def main():
    page = requests.get(SAGA_ORGS)
    tree = etree.HTML(page.content)

    links=tree.xpath('//td/a/@href')

    links=map(lambda x:x.replace('/publishing/','/publishing/AP/'),links)

    for l in links:
        nomealbo=re.sub(r'.*org=','',l)
        print l,nomealbo
        url=SAGA_BASE+l
        page = requests.get(url)
	myparser=etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(page.content,parser=myparser)

        tables=tree.xpath('//table')
        if len(tables)>0:
            table = tables[0]

            data=[]
            rows=table.xpath('*/tr')
            for r in rows[1:]:
                datarow=[]
                for cell in r.xpath('td'):
                    href=cell.xpath('a/@href')
                    text=u''.join(cell.xpath('.//text()')).strip()
                    if len(href) > 0:
                        detailurl=SAGA_BASE+re.sub(r'jsessionid=\S*\?','?',href[0])
                        datarow.append(detailurl)
                    else:
                        datarow.append(text)
                data.append(datarow)

            print data
            outputRSS(nomealbo,data,DIRNAME)
            time.sleep(2)
        else:
            print "ERROR"

if __name__=='__main__':
    main()
