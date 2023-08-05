from .masternode_list_provider import MasternodeListProvider
import random

class MasternodeDiscovery:
    def __init__(self, seeds = None, port = None):
        self.mnlist_provider = MasternodeListProvider(seeds, port)
        self.seeds = seeds


    def get_random_masternode(self, excluded_ips = None):
        # mnlist = self.mnlist_provider.get_mn_list()
        # return random.sample(mnlist, 1)[0]['service']
        
        # Temporary fix till testnet becomes stable
        mnlist = [
            '34.219.81.129',
            '34.221.42.205',
            '34.208.88.128',
            '54.189.162.193',
            '34.220.124.90',
            '54.201.242.241',
            '54.68.10.46',
            '34.210.81.39',
            '18.237.47.243'
            ]
        return random.choice(mnlist)

    def get_mnlist(self):
        return self.mnlist_provider.get_mn_list()


    def check_mn_response(self, ip_address):
        return self.mnlist_provider.check_mn_response(ip_address)


    def reset(self):
        self.mnlist_provider = MasternodeListProvider(self.seeds);
