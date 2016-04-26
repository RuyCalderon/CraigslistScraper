# CraigslistScraper
Prototype of a scraper used to find work on craigslist.

Works by first filling a list of active cities with the static FindActiveCities() method. Then, using the index of a city,
scrapes the craigslist computer gigs section of that city's github page. If the user does not know the index of a particular
city, they can use the .FindCityIndexByName() method to retrieve the necessary index. The data is stored inside the scraper
instance in the .Listings field and can be output to file with the .OutputListingsToFile() method.

*Note: Each time a city is scraped, the internal listings field is cleared, so in between each city, be sure to handle the
data in the manner you see fit to ensure it is not lost.

Available under MIT license, free for anyone to use.
