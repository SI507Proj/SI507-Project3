from bs4 import BeautifulSoup
import unittest
import requests
import logging, sys
import re
from urllib.parse import urljoin

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

######### PART 0 #########

# Write your code for Part 0 here.
def print_alt_txt(website):
    data = requests.get(website).text
    soup = BeautifulSoup(data, 'html.parser')
    # logging.debug(soup)
    imgs = soup.findAll('img')
    # logging.debug(imgs)
    for img in imgs:
        if img.has_attr('alt'):
            print(img['alt'])
        else:
            print("No alternative text provided!")


print_alt_txt("http://newmantaylor.com/gallery.html")


######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable 
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.



# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure 
# that the rest of the program can access.

# TRY: 
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data 
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements


# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.


## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?


# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)


# And then, write each set of data to a file so this won't have to run again.


def cache_site(web_site, cache_file):
    try:
        data = open(cache_file, 'r').read()
    except:
        data = requests.get(web_site).text
        file = open(cache_file, 'w')
        file.write(main_data)
        file.close()
    return data


main_page = "https://www.nps.gov/index.htm"
main_data = cache_site(main_page, "nps_gov_data.html")
soup = BeautifulSoup(main_data, 'html.parser')

search_ul = soup.find('ul', attrs={'class': "dropdown-menu SearchBar-keywordSearch"})
search_lis = search_ul.find_all('li')
# logging.debug(search_lis)

states = ["Arkansas", "California", "Michigan"]
links = {}
for li in search_lis:
    search_a = li.find('a')
    if search_a.text in states:
        link = search_a['href']
        full_link = urljoin(main_page, link)
        # logging.debug(full_link)
        links[search_a.text] = full_link

ar_data = cache_site(links["Arkansas"], "arkansas_data.html")
ca_data = cache_site(links["California"], "california_data.html")
mi_data = cache_site(links["Michigan"], "michigan_data.html")


######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state?
#  How is it organized in HTML?

ar_soup = BeautifulSoup(ar_data, "html.parser")
ca_soup = BeautifulSoup(ca_data, "html.parser")
mi_soup = BeautifulSoup(mi_data, "html.parser")

# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation!
#  So, of course, might be .find or .find_all, etc...

#logging.debug(ar_soup.prettify())
#logging.debug(ca_soup.prettify())
#logging.debug(mi_soup.prettify())

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state,
#  but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park.
#  However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition,
#  you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions
#  -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...



## Define your class NationalSite here:


class NationalSite(object):

    # precond: soup is li object under ul with id "list-parks"
    def __init__(self, soup):
        self.location = soup.find('h4').text
        self.name = soup.find('a').text
        logging.debug(self.name)
        # find park type in h2
        self.type = None
        if soup.find('h2'):
            self.type = soup.find('h2').text

        # find description in p
        self.description = ""
        if soup.find('p'):
            self.description = soup.find('p').text.strip()

        # logging.debug(self.description)

        # find basic info link which has address info
        links = soup.find_all('a')
        self.basic_info = None
        for link in links:
            if "Basic Information" in link.text.strip():
                self.basic_info = link
        # logging.debug(self.basic_info.text)

    def __str__(self):
        return self.name + " | " + self.location

    def get_mailing_address(self):
        link = self.basic_info['href']
        logging.debug(link)
        info = requests.get(link).text
        info_soup = BeautifulSoup(info, 'html.parser')
        try:
            info_div = info_soup.find(id="BasicInfoAccordion")
            addr_div = info_div.find('div', attrs={'class': "physical-address"})
        except:
            addr_div = info_soup.find('div', attrs={'class': "mailing-address"})

        addr_elements = []
        if addr_div:
            addr_elements = addr_div.text.strip().split("\n")
            logging.debug(addr_elements)

        address = ""
        for element in addr_elements:
            # leading and trailing characters removed
            element = element.strip()
            if element:
                address += element + " / "
        if address:
            address = address[0:-2]
        logging.debug(address)
        return address

        #spans = addr_div.find_all('span')
        #for span in spans:
        #    if not span.find('span'):
        #        address += span.text.strip().replace("\n", "") + "/"

        #addr_div = info_soup.find('div', attrs={'class':"mailing-address"})
        #loggin.debug(addr_div)
        #logging.debug(address)
        #return address
        #spans = addr_div.find_all('span')
        #address = ""
        #for span in spans:
        #    if not span['itemprop'].find('span'):
        #        address += span.text.strip().replace("\n", "") + "/"

    def __contains__(self, str):
        return str in self.name



## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:

f = open("sample_html_of_park.html",'r')
soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
sample_inst = NationalSite(soup_park_inst)
sample_inst.get_mailing_address()
f.close()
print(sample_inst)

######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

ar_park_soup = ar_soup.find(id="list_parks").find_all('li', attrs={'class': 'clearfix'})
arkansas_natl_sites = []
for park_soup in ar_park_soup:
    park = NationalSite(park_soup)
    arkansas_natl_sites.append(park)

ca_park_soup = ca_soup.find(id="list_parks").find_all('li', attrs={'class': 'clearfix'})
california_natl_sites = []
# logging.debug(ca_park_soup)
for park_soup in ca_park_soup:
    park = NationalSite(park_soup)
    california_natl_sites.append(park)

mi_park_soup = mi_soup.find(id="list_parks").find_all('li', attrs={'class': 'clearfix'})
michigan_natl_sites = []
# logging.debug(mi_park_soup)
for park_soup in mi_park_soup:
    park = NationalSite(park_soup)
    michigan_natl_sites.append(park)



##Code to help you test these out:
for p in california_natl_sites:
 	print(p)
for a in arkansas_natl_sites:
 	print(a)
for m in michigan_natl_sites:
 	print(m)



######### PART 4 #########

## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!


def create_csv_file(file_name, list):
    with open(file_name, 'w') as csv_file:
        csv_file.write('Name, Location, Type, Address, Description\n')
        for piece in list:
            type = piece.type
            if not type:
                type = "None"
            csv_file.write('\"{}\", \"{}\", {}, \"{}\", \"{}\"\n'.format(piece.name, piece.location,
                           type, piece.get_mailing_address(), piece.description))


create_csv_file('arkansas.csv', arkansas_natl_sites)
create_csv_file('california.csv', california_natl_sites)
create_csv_file('michigan.csv', michigan_natl_sites)