from lxml import html
import requests
import re
import rssmanager as RSS
import time

SAGA_BASE="http://pubblicazioni.saga.it"
SAGA_ORGS=SAGA_BASE+"/orgs/"
BASE_OUT_URL='opendata.matteofortini.it/rssAlboPOP/saga'
DIRNAME='/var/www/opendata.matteofortini.it/rssAlboPOP'

def outputRSS(alboName,data,dirName):
    rss=RSS.rssElaboraNuovi("alboPOP"+alboName,title='alboPOP di '+alboName,base_url=BASE_OUT_URL)
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

    rss.out_rss(alboName+'.xml')

def main():
    page = requests.get(SAGA_ORGS)
    tree = html.fromstring(page.content)

    links=tree.xpath('//td/a/@href')

    links=map(lambda x:x.replace('/publishing/','/publishing/AP/'),links)

    for l in links:
        nomealbo=re.sub(r'.*org=','',l)
        print l,nomealbo
        url=SAGA_BASE+l
        page = requests.get(url)
        tree = html.fromstring(page.content)

        tables=tree.xpath('//table')
        if len(tables)>0:
            table = tables[0]

            data=[]
            rows=table.xpath('*/tr')
            for r in rows[1:]:
                datarow=[]
                for cell in r.xpath('td'):
                    href=cell.xpath('a/@href')
                    text=''.join(cell.xpath('.//text()')).strip()
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