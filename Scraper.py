import requests
from bs4 import BeautifulSoup
from time import sleep
import datetime
import random

def RemoveEncodingSignature(string):
	LocalStringCopy = ''
	
	EncodingState = [{'Type': None, 'Active' : False, 'Delimiter' : None, 'StartingIndex': 0}]
	
	for Index in range(0, len(string)):
		if EncodingState[len(EncodingState) - 1]['Active']:
			if string[Index] != EncodingState[len(EncodingState) - 1]['Delimiter']:
				LocalStringCopy += string[Index]
			else:
				if Index != EncodingState[len(EncodingState) -1]['StartingIndex'] + 1:
					LastState = EncodingState.pop()
					assert(len(EncodingState) > 0)
		elif string[Index] == 'b':
			if Index + 1 < len(string):
				if string[Index + 1] == '\'':
					EncodingState.append({'Type': 'Bytes', 'Active' : True, 'Delimiter' : '\'', 'StartingIndex' : Index})
				if string[Index + 1] == '\"':
					EncodingState.append({'Type': 'Bytes', 'Active' : True, 'Delimiter' : '\"', 'StartingIndex' : Index})
		else:
			LocalStringCopy += string[Index]
	return LocalStringCopy

CraigslistCities = []


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
			CraigslistCities.append({'Name' : cityItem.string , 'URL': url})

random.seed()

#things to watch out for - identical listings being posted in different cities
#think about adding mulitiered keywords, ie; keywords that can stand on their own and others that need other keywords to be valid

KeyWords = ['javascript', 'c++', 'c/c++', 'programmer', 'coder', 'developer', 'python', 'html', 'css', 'tutoring', 'tutor', 'project', 'problem', 'help']
GoodListings = []
StartTime = datetime.datetime.today()
CurrentCityIndex = 0

for City in CraigslistCities:
	sleep(random.uniform(10,17))
	try:
		try:
			CityResponse = requests.get("https:" + City['URL'] + 'search/cpg')
			print("http:" + City['URL'] + 'search/cpg')
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
				
				if (StartTime - DateTimePosted) > datetime.timedelta(days=1):
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
							GoodListings.append({'TimePosted': TimePostedData, 'ListingID': ListingID, 'ListingTitle': ListingTitle, 'ListingLink': City['URL'] + ListingLinkSuffix})
					MoveToNextListing = True
	except Exception as e:
		print(str(e))
	CurrentCityIndex+=1

fouthandle = open('CraigslistResults.txt', 'w')
for Listing in GoodListings:
	NewLine = str(Listing['TimePosted'].encode('utf-8')) + ', ' + str(Listing['ListingTitle'].encode('utf-8')) + ', ' + str(Listing['ListingLink'].encode('utf-8')) + '\n'
	NewLine = RemoveEncodingSignature(NewLine)
	fouthandle.write(NewLine)
fouthandle.close()
print('Finished')
