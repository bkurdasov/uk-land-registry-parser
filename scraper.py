"""
A script to parse UK land registry. Given a list of Title numbers in input.txt, it scrapes address and tenure information and saves it in output.csv
Script uses requests for data fetching and lxml for parsing purposes.
"""
import requests
from lxml.html import fromstring
import csv
uri='https://eservices.landregistry.gov.uk/wps/portal/Property_Search'
s=requests.Session()
page=s.get(uri,allow_redirects=True)
doc=fromstring(page.text)
detailed_uri=doc.xpath('//a[@class="bodylinkcopy"]')[0].get('href')
page2=s.get(u'https://eservices.landregistry.gov.uk/'+detailed_uri)
doc2=fromstring(page2.text)
post_uri=doc2.xpath('//form')[0].get('action')
with open('output.csv','w') as outfile,open('input.txt','r') as infile:
	writer=csv.writer(outfile)
	writer.writerow(['TitleNo','Address line 1','Address line 2','Address line 3','Postcode','Tenure'])
	for line in infile:
	#for _title in  ['SY501298', 'SY729349','SY729377','SY729378']:
		title=line.strip()
		post_data={'enquiryType':'detailed','titleNo':title}
		result=s.post(u'https://eservices.landregistry.gov.uk/'+post_uri,post_data)
		doc3=fromstring(result.text)
		tenure=doc3.xpath('//div[@class="w80p left floatRight"]')[0].text.strip()
		address=doc3.xpath('//div[@class="w80p  left floatRight"]/text()')
		if len(address)<4: address=['']*(4-len(address))+address
		print [title]+address+[tenure]
		writer.writerow([title]+address+[tenure])