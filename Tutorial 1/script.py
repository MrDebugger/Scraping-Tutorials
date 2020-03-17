import requests
import csv
from bs4 import BeautifulSoup
url = 'https://locations.fivebelow.com/'
r = requests.get(url)
soup = BeautifulSoup(r.text,'lxml')
links = soup.findAll(class_='Directory-listLink')

print("Scraping State Links")
states = []
for link in links:
	states.append(url+link.get('href'))
	print("State:",link.text)

print("\nScraping City Links")
cities = []
for state in states:
	if '/' in state.split('.com/')[-1]:
		cities.append(state)
		continue
	r = requests.get(state)
	soup = BeautifulSoup(r.text,'lxml')
	links = soup.findAll(class_='Directory-listLink')
	for city in links:
		cities.append(url+city.get('href'))
		print("City:",city.text)
print("\n\nScraping Stores Links")
stores = []
for city in cities:
	r = requests.get(city)
	soup = BeautifulSoup(r.text,'lxml')
	if soup.find(class_='Hero-name'):
		stores.append(city)
		continue
	links = soup.findAll(class_='Teaser-titleLink')
	for store in links:
		print("Store:",store.text)
		stores.append(url+store.get('href').replace('../',''))
with open('stores.csv','w',encoding='utf-8',newline='') as file:
	csvFile = csv.writer(file)
	csvFile.writerow(['Name','Phone','Store Name','City','Country','Zip Code'])
	for store in stores:
		r = requests.get(store)
		soup = BeautifulSoup(r.text,'lxml')
		name = soup.find(class_='Hero-locationGeo').text.strip()
		p = soup.find('div',{'itemprop':'telephone'})
		if p:
			phone = p.text.strip()
		else:
			phone = 'No Found'
		stAddr = soup.find(class_='c-address-street-1').text.strip()
		city = soup.find(class_='c-address-city').text.strip()
		state = soup.find(class_='c-address-state').text.strip()
		country = soup.find('abbr',{'itemprop':'addressCountry'}).get('title')
		zipcode = soup.find(class_='c-address-postal-code').text.strip()
		csvFile.writerow([name,phone,stAddr,city,country,zipcode])
		print([name,phone,stAddr,city,country,zipcode])
print("DONE")