#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import logging
import pprint
import dns.resolver
import json


pp = pprint.PrettyPrinter(indent=2)

class PrettyLog():
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return pprint.pformat(self.obj)


def getArgs():
    '''This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(
        description='Script to test dnsmasq for Zabbix')
    parser.add_argument('--dnsmasq', help='DNSmasq Listen address', required=False, type=str, default='127.0.0.1')
    parser.add_argument('--dnsmasqport', help='DNSmasq Listen address', required=False, type=int, default=53)
    parser.add_argument('--leasespath', help='path to the dnsmasq leases file', required=False, type=str, default='/var/lib/misc/dnsmasq.leases')
    parser.add_argument('--metricname', help='Metric name to gather: cachesize.bind.,insertions.bind.,evictions.bind.,misses.bind.,hits.bind.,auth.bind.,servers.bind.', required=True, type=str)
    parser.add_argument('--queriesfails', help='Show number of queries failed in the server instead successfull queries in servers.bind. metric', required=False, action='store_true')
    parser.add_argument(
        '-v', '--verbose', help="Be verbose", action="store_const", dest="loglevel", const=logging.DEBUG)
    args = parser.parse_args()
    return args

metrics = {
    "cachesize.bind." : {
        "name": "dnsmasq_cachesize",
		"help": "configured size of the DNS cache"},
    "insertions.bind.": {
        "name": "dnsmasq_insertions",
		"help": "DNS cache insertions"},
    "evictions.bind.": {
        "name": "dnsmasq_evictions",
		"help": "DNS cache exictions: numbers of entries which replaced an unexpired cache entry"},
    "misses.bind.": {
        "name": "dnsmasq_misses",
		"help": "DNS cache misses: queries which had to be forwarded"},
    "hits.bind.": {
        "name": "dnsmasq_hits",
		"help": "DNS queries answered locally (cache hits)"},
    "auth.bind.": {
        "name": "dnsmasq_auth",
		"help": "DNS queries for authoritative zones"},
    "servers.bind.":{
        "name": "dnsmasq_servers",
        "help": "DNS queries statistics per server"},
}

# servermetrics = {
#     "queries" : {
#         "value" : 0,
#         "name" : "dnsmasq_servers_queries",
#         "help": "DNS queries on upstream server"},
#     "queries_failed": {
#         "value" : 0,
#         "name" : "dnsmasq_servers_queries_failed",
#         "help": "DNS queries failed on upstream server"},
#     "leases" : {
#         "name": "dnsmasq_leases",
# 	    "help": "Number of DHCP leases handed out",}
# }

def getMetrics(dnsserver, dnsport, metricname):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 5
    resolver.lifetime = 5

    if not metricname.endswith('.'): # Add trailing dot in case you forget.
        metricname += '.'

    datametrtics = ''
    if metricname in metrics and dnsserver:
        resolver.nameservers = [dnsserver]
        resolver.port = dnsport
        try:
            #result = resolver.query(metricname, '')
            result = resolver.query(qname=metricname, rdclass="CHAOS", rdtype="TXT")

            for item in result.rrset.items:
                """ Remove quotes from output and split every server in arrays.
                    From this "10.1.0.64#53 18850 109" "10.1.0.63#53 20818 100" "10.4.10.3#53 1173 69"
                    to [['10.1.0.64#53', '18874', '109'],['10.1.0.63#53', '20864', '100'],['10.4.10.3#53', '1173', '69']]
                """
                if metricname == 'servers.bind.':
                    data = [i.split(" ") for i in [i.strip() for i in item.to_text().split("\"")] if i]
                    logger.debug("Data: " + str(data))
                    numqueries = 0
                    numqueriesfail = 0
                    for queries in data:
                        numqueries += int(queries[1])
                        numqueriesfail += int(queries[2])
                    if args.queriesfails:
                        datametrtics = numqueriesfail
                    else:
                        datametrtics = numqueries
                        
                else:
                    data = item.to_text().replace("\"", "")
                    datametrtics = data
        except dns.exception.Timeout:
            logger.error("DNS Timeout for {} using {}".format( metricname, dnsserver))
            resolver.nameservers.remove(args.dnsmasq)
            return False
        except dns.resolver.NXDOMAIN:
            logger.error("[.] Resolved but no entry for " + str(metricname))
            resolver.nameservers.remove(args.dnsmasq)
        except dns.resolver.NoNameservers:
            logger.error("[-] Answer refused for " + str(metricname))
        except dns.resolver.NoAnswer:
            logger.error("[-] No answer section for " + str(metricname))
    elif metricname == 'leases':
        try:
            with open(args.leasespath, 'r') as fp:
                datametrtics = len(fp.readlines())
        except FileNotFoundError:
            logger.info("[!] File not found " + args.leasespath)


    logger.debug("Data: " + str(datametrtics))
    print(datametrtics)


if __name__ == "__main__":
    args = getArgs()
    logging.basicConfig(level=args.loglevel,
                    format='%(asctime)s %(name)-13s (%(process)-4d) %(levelname)-7s- %(message)s')
    logger = logging.getLogger('zabbix_dnsmasq')
    #logger.error("Init.")
    getMetrics( args.dnsmasq, args.dnsmasqport, args.metricname)

