import requests

def getLiveData(bus_number):
    url = "https://store.transitstat.us/passio_go/rutgers/trains"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get(bus_number)  # Return data for the specific bus
    else:
        print("Error fetching data:", response.status_code)
        return None

if __name__ == "__main__":
    bus_to_check = input("Enter a bus number to check: ")
    bus_data = getLiveData(bus_to_check)

    if bus_data:
        print("Data for bus", bus_to_check, ":")
        print(bus_data)
    else:
        print("Bus", bus_to_check, "not found in the data.")