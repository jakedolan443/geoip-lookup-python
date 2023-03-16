from os import listdir
from os.path import isfile, join
import ipaddress
import json


class GeoIPLookup:
    def __init__(self, disk_only=False):
        self.config = {"disk_only":disk_only}
        
        self.__ip_dict = {}
        
        # in disk_only mode, the geoip database will NOT be loaded into memory.
        # this will inevitably lead to longer query times, but allows the package
        # to run lightweight on systems with less memory available.
        
        # note, the database will take up to 300MB of memory if this mode is not
        # specified.

        if not self.config['disk_only']:
            
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
            # optimise the dict for fastest access
            self.__optimise()
            
    def __optimise(self):
        print("done!")
        if not self.config['disk_only']:
            print(self.query("1.5.1.25"))
            print(self.query("7.64.6.32"))
            print(self.query("88.124.42.1"))
            print(self.query("121.51.21.15"))
            print(self.query("51.41.211.51"))
            print(self.query("78.21.21.41"))
            
    def query(self, address):
        address = int(ipaddress.IPv4Address(address))
        halves = list(map(''.join, zip(*[iter(str(address))]*4)))
        halves[1] = halves[1][:2]
        for entry in self.__ip_dict[halves[0]][halves[1]]:
            return entry


    




