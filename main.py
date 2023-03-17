from os import listdir
from os.path import isfile, join
import ipaddress
import json


class GeoIPLookup:
    def __init__(self):
        self.__ip_dict = {}
            
        # load the database into memory.
        for country in [f for f in listdir("index/") if isfile(join("index/", f))]:
            with open("index/{}".format(country), "r") as f:
                data = json.loads(f.read())
                for entry in data:
                    halves = list(map(''.join, zip(*[iter(str(entry[0]))]*4)))
                    halves[1] = halves[1][:2]
                    try:
                        self.__ip_dict[halves[0]][halves[1]].append(entry)
                    except KeyError:
                        try:
                            self.__ip_dict[halves[0]][halves[1]] = [entry]
                        except KeyError:
                            self.__ip_dict[halves[0]] = {halves[1]:[entry]}
            
    def query(self, address):
        address = int(ipaddress.IPv4Address(address))
        halves = list(map(''.join, zip(*[iter(str(address))]*4)))
        halves[1] = halves[1][:2]
        to_search = []
        for entry in self.__ip_dict[halves[0]][halves[1]]:
            to_search.append(entry)
        for entry in to_search:
            if address > int(entry[0]):
                if address < int(entry[1]):
                    return entry
        return []


if __name__ == "__main__":
    ip = GeoIPLookup()
    print(ip.query("8.8.8.8"))
    




