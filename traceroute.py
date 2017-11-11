import socket
import sys
import json
import pickle
from datetime import datetime
#Non standard import
from scapy.all import *
import requests


#Some global vars

dicc_country_continent = {"AD": "Europe","AE": "Asia","AF": "Asia","AG": "America","AI": "America","AL": "Europe","AM": "Asia","AN": "America","AO": "Africa","AQ": "Antarctica","AR": "America","AS": "Oceania","AT": "Europe","AU": "Oceania","AW": "America","AZ": "Asia","BA": "Europe","BB": "America","BD": "Asia","BE": "Europe","BF": "Africa","BG": "Europe","BH": "Asia","BI": "Africa","BJ": "Africa","BM": "America","BN": "Asia","BO": "America","BR": "America","BS": "America","BT": "Asia","BW": "Africa","BY": "Europe","BZ": "America","CA": "America","CC": "Asia","CD": "Africa","CF": "Africa","CG": "Africa","CH": "Europe","CI": "Africa","CK": "Oceania","CL": "America","CM": "Africa","CN": "Asia","CO": "America","CR": "America","CU": "America","CV": "Africa","CX": "Asia","CY": "Asia","CZ": "Europe","DE": "Europe","DJ": "Africa","DK": "Europe","DM": "America","DO": "America","DZ": "Africa","EC": "America","EE": "Europe","EG": "Africa","EH": "Africa","ER": "Africa","ES": "Europe","ET": "Africa","FI": "Europe","FJ": "Oceania","FK": "America","FM": "Oceania","FO": "Europe","FR": "Europe","GA": "Africa","GB": "Europe","GD": "America","GE": "Asia","GF": "America","GG": "Europe","GH": "Africa","GI": "Europe","GL": "America","GM": "Africa","GN": "Africa","GP": "America","GQ": "Africa","GR": "Europe","GS": "Antarctica","GT": "America","GU": "Oceania","GW": "Africa","GY": "America","HK": "Asia","HN": "America","HR": "Europe","HT": "America","HU": "Europe","ID": "Asia","IE": "Europe","IL": "Asia","IM": "Europe","IN": "Asia","IO": "Asia","IQ": "Asia","IR": "Asia","IS": "Europe","IT": "Europe","JE": "Europe","JM": "America","JO": "Asia","JP": "Asia","KE": "Africa","KG": "Asia","KH": "Asia","KI": "Oceania","KM": "Africa","KN": "America","KP": "Asia","KR": "Asia","KW": "Asia","KY": "America","KZ": "Asia","LA": "Asia","LB": "Asia","LC": "America","LI": "Europe","LK": "Asia","LR": "Africa","LS": "Africa","LT": "Europe","LU": "Europe","LV": "Europe","LY": "Africa","MA": "Africa","MC": "Europe","MD": "Europe","ME": "Europe","MG": "Africa","MH": "Oceania","MK": "Europe","ML": "Africa","MM": "Asia","MN": "Asia","MO": "Asia","MP": "Oceania","MQ": "America","MR": "Africa","MS": "America","MT": "Europe","MU": "Africa","MV": "Asia","MW": "Africa","MX": "America","MY": "Asia","MZ": "Africa","NA": "Africa","NC": "Oceania","NE": "Africa","NF": "Oceania","NG": "Africa","NI": "America","NL": "Europe","NO": "Europe","NP": "Asia","NR": "Oceania","NU": "Oceania","NZ": "Oceania","OM": "Asia","PA": "America","PE": "America","PF": "Oceania","PG": "Oceania","PH": "Asia","PK": "Asia","PL": "Europe","PM": "America","PN": "Oceania","PR": "America","PS": "Asia","PT": "Europe","PW": "Oceania","PY": "America","QA": "Asia","RE": "Africa","RO": "Europe","RS": "Europe","RU": "Europe","RW": "Africa","SA": "Asia","SB": "Oceania","SC": "Africa","SD": "Africa","SE": "Europe","SG": "Asia","SH": "Africa","SI": "Europe","SJ": "Europe","SK": "Europe","SL": "Africa","SM": "Europe","SN": "Africa","SO": "Africa","SR": "America","ST": "Africa","SV": "America","SY": "Asia","SZ": "Africa","TC": "America","TD": "Africa","TF": "Antarctica","TG": "Africa","TH": "Asia","TJ": "Asia","TK": "Oceania","TM": "Asia","TN": "Africa","TO": "Oceania","TR": "Asia","TT": "America","TV": "Oceania","TW": "Asia","TZ": "Africa","UA": "Europe","UG": "Africa","US": "America","UY": "America","UZ": "Asia","VC": "America","VE": "America","VG": "America","VI": "America","VN": "Asia","VU": "Oceania","WF": "Oceania","WS": "Oceania","YE": "Asia","YT": "Africa","ZA": "Africa","ZM": "Africa","ZW": "Africa"}
GEOIPURL = "http://www.freegeoip.net/json/"

#Router Class
class Router:
	"""docstring for hopers"""
	def __init__(self, host_ip, rtt, hop_number):
		self.ip_address = host_ip
		self.rtt = rtt
		self.continent = 'null'
		self.salto_intercontinental = 'false'
		self.salto_intercontinental_by_api = 'false'
		self.hop_num = hop_number

#Some utils functions

def host_to_ip(hostname):
	return socket.gethostbyname(hostname)

# returns a list of tuples with routers ip and rtt
def routers_in_specific_ttl(dest,ttl,rafaga):
	routers = []
	llegue = False
	for i in range(rafaga):
		packet = IP(dst=dest,ttl=ttl) / ICMP ()
		ans,unans = sr(packet, verbose=0)
		sent = datetime.fromtimestamp(ans[0][0].sent_time)
		recived = datetime.fromtimestamp(ans[0][1].time)
		rtt = (recived - sent).total_seconds() * 1000
		if ans[0][1].sprintf('%type%') == '11':
			r = ans[0][1].sprintf('%src%')
			routers.append((r,rtt))
		if ans[0][1].sprintf('%type%') == '0':
			r = ans[0][1].sprintf('%src%')
			routers.append((r,rtt))
			llegue = True
		#if ans[0][1].sprintf('%type%') == '':
		#	pass
	return routers, llegue

#return host ip, rtt
def sacar_host_mediana(list_of_host):
	list_of_host.sort(key=lambda tup: tup[1])
	median_index = len(list_of_host)/2
	return list_of_host[median_index][0], list_of_host[median_index][1]



def continent_of_ip(router_ip):
	try:
		req = requests.get(GEOIPURL+router_ip)
		req.raise_for_status()
	except requests.exceptions.HTTPError:
		print 'Error en el request'
		return 'null'
	else:
		try:
			data = json.loads(req.text)
		except ValueError:
			print "Invalid JSON Object"
			return 'null'
		else:
			if data['country_code'] == "":
				return 'null'
			else:
				return dicc_country_continent[data['country_code']]

def outliers(list_of_host):
	pass

def printear_a_json():
	pass

def what_continent_belong(list_of_host):
	list_of_host[0].salto_intercontinental_by_api = 'false'
	for indice in range(1,len(list_of_host)):
		list_of_host[indice].continent = continent_of_ip(list_of_host[indice].ip_address)
		if list_of_host[indice-1].continent == 'null' or list_of_host[indice].continent == 'null':
			list_of_host[indice].is_intercontinental = 'null'	 
		else:
			list_of_host[indice].salto_intercontinental_by_api = str(list_of_host[indice-1].continent != list_of_host[indice].continent)

def traceroute(dest,rafaga):
	try:
		socket.inet_aton(dest)
	except socket.error:
		try:
			dest = host_to_ip(dest)
		except socket.gaierror:
			print "No entendi ese host"
			return 1
	list_of_host = []
	#Set max ttl to 32 cause traceroute default does that
	for ttl in range(1,32):
		host_rafaga, llegue = routers_in_specific_ttl(dest,ttl,rafaga)
	 	hop_ip,rtt = sacar_host_mediana(host_rafaga)
		router_temp = Router(hop_ip,rtt,ttl)
		list_of_host.append(router_temp)
		if llegue:
			break
	# So here I have my list of routers in each ttl iteration
	# then we need to know which continent belongs
	what_continent_belong(list_of_host)
	list_para_json = []
	for i in range(len(list_of_host)):
		dicc_para_json={"rtt":list_of_host[i].rtt, "ip_address":list_of_host[i].ip_address, "salto_intercontinental":list_of_host[i].salto_intercontinental, "hop_number":list_of_host[i].hop_num}
		list_para_json.append(dicc_para_json)

	print json.dumps(list_para_json, indent=2)
	#for l in list_of_host:
	#	print l.ip_address,
	#	print l.rtt,
	#	print l.continent,
	#	print l.salto_intercontinental,
	#	print l.salto_intercontinental_by_api,
	#	print l.hop_num
	# So now we need to apply the algorith to detect outliers based in rtt
	#outliers(list_of_host)
	#printear_a_json(list_of_host)

if __name__ == '__main__':
	arg = sys.argv[1:]
	dest = arg[0]
	rafaga = arg[1]
	traceroute(dest,int(rafaga))
