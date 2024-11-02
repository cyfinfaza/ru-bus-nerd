# %%
import requests
import pandas as pd
from bs4 import BeautifulSoup

class UserFacingError(Exception):
    def __init__(self, message):
        self.message = message

def scrapeByNum(bus_number):
    try:
        html = requests.get('https://cptdb.ca/wiki/index.php/Rutgers_University').content

        df_list = pd.read_html(html)
        soup = BeautifulSoup(html, 'html.parser')
        for br in soup.find_all("br"):
            br.replace_with("\n")
        current_fleet = list(filter(lambda x: "Fleet Number(s)" in x, df_list))[0]

        def testRanges(bus_num):
            for entry in current_fleet["Fleet Number(s)"]:
                for num in entry.split(","):
                    try:
                        if not "-" in num:
                            if bus_num == int(num):
                                return entry
                        else:
                            if bus_num in range(int(num.split("-")[0]), int(num.split("-")[1])+1):
                                return entry
                    except ValueError as e:
                        print(e)
                        print("Failed to parse bus number group with string " + num)
            raise UserFacingError("Bus number not found.")

        bus_data = {}
        bus_set = testRanges(bus_number)
        bus_data['group'] = bus_set
        link = soup.findAll('a', href=True, string=bus_set)[0]
        mainpage_data_row = list(map(lambda x: x.text.replace("\n", " ").strip(), link.findParents('tr')[0].findAll('td')))
        mainpage_header_row = list(map(lambda x: x.text.replace("\n", " ").strip().lower(), link.findParents('table')[0].findAll('th')))
        bus_data.update(dict(zip(mainpage_header_row[1:], mainpage_data_row[1:])))
        if 'notes' in bus_data:
            bus_data['group_notes'] = bus_data['notes']
            del bus_data['notes']
        to_url = "https://cptdb.ca" + link['href']

        bus_page = requests.get(to_url).content
        bus_soup = BeautifulSoup(bus_page, 'html.parser')
        for br in bus_soup.find_all("br"):
            br.replace_with("\n")

        # %%
        def findFleetNumCell(fleet_num):
            for cell in bus_soup.findAll('td'):
                try:
                    if fleet_num == int(cell.text):
                        return cell
                except:
                    pass
        fleet_num_row = findFleetNumCell(bus_number).findParents('tr')[0]
        buspage_data_row = list(map(lambda x: x.text.replace("\n", " ").strip(), fleet_num_row.findAll('td')))
        buspage_header_row = list(map(lambda x: x.text.replace("\n", " ").replace("/", "_").replace("(", "").replace(")", "").strip().lower().replace(" ", "_"), findFleetNumCell(bus_number).findParents('table')[0].findAll('th')))
        bus_data.update(dict(zip(buspage_header_row, buspage_data_row)))

        # %%
        if 'thumbnail' in bus_data:
            del bus_data['thumbnail']
        if len(fleet_num_row.findAll('img')) > 0:
            img_url = "https://cptdb.ca/wiki/images/" + "/".join(fleet_num_row.findAll('img')[0]['src'].split("/")[-4:-1])
            bus_data['image_url'] = img_url
        else:
            bus_data['image_url'] = None

        notes_column = buspage_header_row.index('notes')
        bus_notes = fleet_num_row('td')[notes_column].text.strip()
        bus_data['notes'] = bus_notes

        return bus_data
    except UserFacingError as e:
        raise Exception(e.message) from e
    except Exception as e:
        print(e)
        raise Exception("Internal error") from e

if __name__ == "__main__":
    test_bus = int(input("Enter a bus number: "))
    print(scrapeByNum(test_bus))