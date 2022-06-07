# zabbix_dnsmasq
DNSmasq monitoring for Zabbix

# Instalation
Copy externalscript content in /usr/local/bin/
Copy zdnsmasq.conf in zabbix agent configuracion in /etc/zabbix/zabbix_agent2.d
Restar Zabbix agent: systemctl restart zabbix-agent2.service
Import in Zabbix server template file template-zdnsmasq.json.
