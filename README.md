# zabbix_dnsmasq
DNSmasq monitoring for Zabbix

# Instalation
- Copy externalscript content in /usr/local/bin/
- Copy zdnsmasq.conf in zabbix agent configuracion in /etc/zabbix/zabbix_agent2.d
- Restar Zabbix agent: systemctl restart zabbix-agent2.service
- Import in Zabbix server template file template-zdnsmasq.json.
- Install dns library: sudo apt install python3-dnspython

# Items collected

|Name|Description|Type|Key and additional info|
|----|-----------|----|----|
|Server queries fails|Total DNS queries failed on upstream servers.|`Zabbix agent`|zdnsmasqfail["{$DNS.SERVER}","{$DNS.PORT}","servers.bind."]|
|Server queries|Total DNS queries on upstream servers.|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","servers.bind."]|
|Misses|DNS cache misses: queries which had to be forwarded.|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","misses.bind."]|
|Insertions|DNS cache insertions.|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","insertions.bind."]|
|Hits|number of requests served by the dnsmasq from its cache|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","hits.bind."]|
|Evictions|DNS cache exictions: numbers of entries which replaced an unexpired cache entry|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","evictions.bind."]|
|Cachesize|Configured size of the DNS cache.|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","cachesize.bind."]|
|Authoritative zones|DNS queries for authoritative zones|`Zabbix agent`|zdnsmasq["{$DNS.SERVER}","{$DNS.PORT}","auth.bind."]|
