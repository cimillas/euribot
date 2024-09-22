import requests
from bs4 import BeautifulSoup
from datetime import date

URL_EURIBOR_12m = 'https://www.euribor-rates.eu/es/tipos-euribor-actualmente/4/euribor-valor-12-meses/'
URL_EURIBOR_6m 	= 'https://www.euribor-rates.eu/es/tipos-euribor-actualmente/3/euribor-valor-6-meses/'

def _scrapEuribor(html):
	page = BeautifulSoup(html, 'html.parser')
	today = date.today()
	values = page.find('h2').find_parent().find_next_sibling().find_all('tr')
	
	for entry in values:
		td_date = entry.next_element.text.strip()
		if td_date == today:
			return entry.find('td', class_='text-right').text.strip()
	else:
		return values[0].find('td', class_='text-right').text.strip() #if today is holyday, returning most recent value

	
def retrieveEuriborValue(url):
	try:
		response = requests.get(url)
		response.raise_for_status()
	except requests.exceptions.HTTPError as http_err:
		print(f"HTTP error occurred: {http_err}")
	except requests.exceptions.ConnectionError as conn_err:
		print(f"Connection error occurred: {conn_err}")
	except requests.exceptions.Timeout as timeout_err:
		print(f"Timeout error occurred: {timeout_err}")
	except requests.exceptions.RequestException as req_err:
		print(f"An error occurred: {req_err}")
	
	return _scrapEuribor(response.text)

if __name__ == '__main__':
	print(retrieveEuriborValue(URL_EURIBOR_12m))
	print(retrieveEuriborValue(URL_EURIBOR_6m))


	
		

	