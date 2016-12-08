from lxml import etree

from feedgen.ext.base import BaseExtension, BaseEntryExtension


def _set_value(channel, name, value):
    if value:
        newelem = etree.SubElement(channel, name)
        newelem.text = value

class AlbopopExtension(BaseExtension):
	def __init__(self):
		self._categoryType=None
		self._categoryName=None

	def extend_rss(self, rss_feed):
		CC='http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html'
		XHTML='http://www.w3.org/1999/xhtml'
		nsmap={'xhtml':XHTML,'creativeCommons':CC}
		channel = rss_feed[0]
		#channel.set_value(channel, 'creativeCommons:license', 'http://creativecommons.org/licenses/by/4.0/')

		# Copyright
		newelem=etree.SubElement(channel,'{%s}license'%(CC,),nsmap=nsmap)
		newelem.text='http://creativecommons.org/licenses/by/4.0/'

		# xhtml:meta
		newelem=etree.SubElement(channel,'{%s}meta'%(XHTML,),nsmap=nsmap)
		newelem.set('name','robots')
		newelem.set('content','noindex')

		# Channel category country
		newelem=etree.SubElement(channel,'category')
		newelem.set('domain','http://albopop.it/specs#channel-category-country')
		newelem.text='Italy'

		# Channel category type
		if self._categoryType:
			newelem=etree.SubElement(channel,'category')
			newelem.set('domain','http://albopop.it/specs#channel-category-type')
			newelem.text=self._categoryType

		# Channel category name
		if self._categoryName:
			newelem=etree.SubElement(channel,'category')
			newelem.set('domain','http://albopop.it/specs#channel-category-name')
			newelem.text=self._categoryName

	def categoryName(self,name=None):
		self._categoryName=name

	def categoryType(self,name=None):
		self._categoryType=name

class AlbopopEntryExtension(BaseEntryExtension):
	def __init__(self):
		self._categoryUID=None
		self._categoryType=None

	def extend_rss(self, entry):
		# Channel category type
		if self._categoryType:
			newelem=etree.SubElement(entry,'category')
			newelem.set('domain','http://albopop.it/specs#item-category-type')
			newelem.text=self._categoryType

		# Channel category UID
		if self._categoryUID:
			newelem=etree.SubElement(entry,'category')
			newelem.set('domain','http://albopop.it/specs#item-category-uid')
			newelem.text=self._categoryUID

	def categoryUID(self,name=None):
		self._categoryUID=name
