#Deprecated
import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime
import random


class CraigslistCity:
	def __init__(self, Name, URL):
		self.name = Name
		self.url = URL

class CraigslistListing:
	def __init__(self, TimePosted, ID, Title, Link):
		self.TimePosted = TimePosted
		self.Title = Title
		self.Link = Link
		self.ListingID = ID

class Scraper:
	ActiveCities = []
	ActiveCitiesFound = False

	@staticmethod
	def FindActiveCities():
		url = "http://www.craigslist.org/about/sites"
		WebResponse = requests.get(url)

		if WebResponse.status_code == 200:
			#print("Web OK")

			parsedHTML = BeautifulSoup(WebResponse.text, "html.parser")

			if(parsedHTML):
				#print("HTMLparsing OK")

				usadiv = parsedHTML.body.section.find_all('div')[2]
				

				USCities = usadiv.find_all('li')

				for cityItem in USCities:
					url = cityItem.a['href']
					Scraper.ActiveCities.append(CraigslistCity(cityItem.string,"https:" + url + 'search/cpg'))
		
		NumberOfActiveCities = len(Scraper.ActiveCities)
		if NumberOfActiveCities == 0:
			print("Scraper failed to find any active cities")
			return -1

		Scraper.ActiveCitiesFound = True

	@staticmethod
	def SeedTimeout():
		random.seed()

	def __init__(self, Keywords):
		self.SearchKeywords = Keywords
		self.Timeout = [10,17]
		self.MaxListingAge = datetime.timedelta(days=1)

	def __init__(self, Keywords, TimeoutRange, MaxListingAge): #in days
		self.SearchKeywords = Keywords
		self.Timeout = TimeoutRange
		self.MaxListingAge = datetime.timedelta(days=MaxListingAge)

	def RefillKeywords(self, Keywords):
		self.SearchKeywords = keywords

	def ScrapeCity(self, Index):
		self.Listings = []
		StartTime = datetime.datetime.today()
		if not Scraper.ActiveCitiesFound:
			print("Cannot scrape city, no active cities found or static class function FindActiveCities has not been called")
			return -1
		if Index >= 0 and Index < len(Scraper.ActiveCities):
			CityURL = Scraper.ActiveCities[Index].url

			try:
				CityResponse = requests.get(CityURL)
				print(CityURL)
			except:
				print(CurrentCityIndex)
				print(City['URL'])
			if CityResponse.status_code == 200:
				print('ok')
				parsedCityHTML = BeautifulSoup(CityResponse.text,'html.parser')
				MoveToNextListing = True
				FirstListing = True
				Count = 0
				while(MoveToNextListing):
					Count+=1

					if(FirstListing):
						listing = parsedCityHTML.find('p')
						FirstListing = False
					else:
						listing = listing.find_next_sibling('p')

					TimePostedData = listing.find('time')['datetime']
					DateTimePosted = datetime.datetime.strptime(TimePostedData,'%Y-%m-%d %H:%M')
					
					if (StartTime - DateTimePosted) > self.MaxListingAge:
						MoveToNextListing = False
					else:
						ValidListing = False
						
						ListingContainers = listing.find_all('a')
						ListingTitle = ListingContainers[1].text.lower()
						ListingID = ListingContainers[1]['data-id']
						ListingLinkSuffix = ListingContainers[1]['href']
						
						if ListingContainers[1]['class'][0] != 'hdrlnk':
							for container in ListingContainers:
								if container['class'] == 'hdrlnk':
									ListingTitle = container.text
									ListingID = container['data-id']
									ListingLinkSuffix = container['href']
									ValidListing = True
						else:
							ValidListing = True
						
						if ValidListing:
							KeywordFound = False
							for keyword in KeyWords:
								if keyword in ListingTitle:
									KeywordFound = True
							if KeywordFound:
								self.Listings.append(CraigslistListing(TimePostedData, ListingID, ListingTitle, CityURL + ListingLinkSuffix))
						MoveToNextListing = True
			sleep(random.uniform(10,17))

			return 'Success'
		else:
			print('Invalid Index: ' + Index + '\nAllowed range(inclusive) is (')
			if(len(Scraper.ActiveCities) > 0):
				print('0,' + (len(Scraper.ActiveCities) - 1 ))
			print(')')
			return "Error Occured"

	def FindCityIndexByName(CityName):
		if not Scraper.ActiveCitiesFound:
			print("Cannot scrape city, no active cities found or static class function FindActiveCities has not been called")
			return -1
		for CityIndex in range(0,len(Scraper.ActiveCities)):
			if Scraper.ActiveCities[CityIndex].name.lower() == CityName.lower():
				return CityIndex

	def OutputListingsToFile(self, FileName):
		fouthandle = open(FileName, 'w')
		for Listing in self.Listings:
			NewLine = Listing.TimePosted.encode('ascii', 'replace').decode('utf-8') + ', ' + Listing.Title.encode('ascii', 'replace').decode('utf-8') + ', ' + Listing.Link.encode('ascii', 'replace').decode('utf-8') + '\n'
			NewLine.replace('??', '').replace('?', '')
			fouthandle.write(NewLine)
		fouthandle.close()


KeyWords = ['javascript', 'c++', 'c/c++', 'programmer', 'coder', 'developer', 'python', 'html', 'css', 'tutoring', 'tutor', 'project', 'problem', 'help']

TimoutRange = [10,17]
MaxListingAge = 1
ScraperInstance = Scraper(KeyWords, TimoutRange, MaxListingAge)
Scraper.SeedTimeout()
Scraper.FindActiveCities()

#if(Scraper.ActiveCitiesFound):
#	Successes = 0
#	Failures = 0
#	for CityIndex in range(0, 10):
#		Result = ScraperInstance.ScrapeCity(CityIndex)
#		if Result == 'Success':
#			print('ok')
#			Successes+=1
#		else:
#			print("Error occurred while scraping index: " + str(CityIndex) + '\n')
#			ErrorCity = Scraper.ActiveCities[Index].name
#			print("This is: " + ErrorCity.name + '\nURL is: ' + ErrorCity.url)
#			Failures+=1

#print("(Successes, Failures) : (" + str(Successes) + ', ' + str(Failures) + ')')

ChicagoIndex = Scraper.FindCityIndexByName("Chicago")

ScraperInstance.ScrapeCity(ChicagoIndex)

ScraperInstance.OutputListingsToFile("ScraperResults_OOP.txt")
print('Finished')
