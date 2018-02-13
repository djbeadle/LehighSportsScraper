from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import re

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=False)) as resp:
            print(resp)
            if is_good_response(resp):
            	return resp.content
            else:
                print("Bad response")
                print(resp)
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

for i in range (1,500):
	filename = ""
	filename += str(i)
	filename += ".html"
	# print("\n")
	# print(filename)
	raw_html = open("./scraped/" + filename)

	html = BeautifulSoup(raw_html, 'html.parser')
	
	# Get the title:
	sidearm_section = html.find('article', {"class" : "sidearm-schedule sidearm-common"})
	if sidearm_section == None:
		continue
	new_name = sidearm_section.find(['h2']).text
	new_name +=", "
	# print(new_name)

	# Get the game container:
	games = html.find('ul', {"class" : "sidearm-schedule-games-container"})
	rows = games.find_all('li', {"class" : "sidearm-schedule-game"})
	for row in rows:

		#### Date: ####
		data_point = row.find('div', {"class" : "sidearm-schedule-game-opponent-date"})
		
		# Bash it into CSV format!
		if data_point != None:
			date = data_point.text.replace(")\n", ") ")
			date = date.replace("\n", " ")
			date = date.strip()
			date += ","
		else:
			date = ","
		# print(date)

		#### Opponent Name: ####
		data_point2 = row.find("span", {"class" : "sidearm-schedule-game-opponent-name"})
		if data_point2 != None:
			opponent_name = data_point2.text.strip()
			opponent_name = opponent_name.replace(", ", " ")
			opponent_name = opponent_name.replace(",", "")
			opponent_name = opponent_name.replace("\n", " ")
			opponent_name += ","
		else:
			opponent_name = ", "
		# print(opponent_name)

		#### Game Location: ####
		data_point3 = row.find("div", {"class" : "sidearm-schedule-game-location"})
		if data_point3 != None:
			location = data_point3.text.strip()
			location = location.replace("\n", " ")
			location = location.replace(", ", " ")
			location += ","
		else:
			location = ", "
		# print(location)

		#### Game Result: ####
		data_point4 = row.find("div", {"class" : "sidearm-schedule-game-result"})
		if data_point4 != None:
			result = data_point4.text
			result = result.replace("\n", " ")
			result = result.strip()

			if result == "":
				result = "Na, Na"
				break

			if re.search("W|w|L|l|T|t", result) is None:
				result = "Na," + result

			result += ","
		else:
			result = "Na, Na"
		# print(result)

		print(filename, ",", new_name, date, opponent_name, location, result)

	sys.stdout.flush()

	




'''
for entry in entries:
		date = entry.find("div", {"class" : "sidearm-schedule-game-opponent-date"})
		if date != None:
			print(date)



	# Get each game from the table rows:
	rows = html.find('ul', {"class" : "sidearm-schedule-games-container"})
	rows_c = rows.findChildren()
	for row in rows_c:
		dates = row.find_all("div", {"class" : "sidearm-schedule-game-opponent-date"})
		for date in dates:
			if date != None:
				print(date.text)
'''



