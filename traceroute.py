import socket
import sys
import json
import pickle
from datetime import datetime
#Non standard import
from scapy.all import *
import requests
import numpy


#Some global vars

dicc_country_continent = {"AD": "Europe","AE": "Asia","AF": "Asia","AG": "America","AI": "America","AL": "Europe","AM": "Asia","AN": "America","AO": "Africa","AQ": "Antarctica","AR": "America","AS": "Oceania","AT": "Europe","AU": "Oceania","AW": "America","AZ": "Asia","BA": "Europe","BB": "America","BD": "Asia","BE": "Europe","BF": "Africa","BG": "Europe","BH": "Asia","BI": "Africa","BJ": "Africa","BM": "America","BN": "Asia","BO": "America","BR": "America","BS": "America","BT": "Asia","BW": "Africa","BY": "Europe","BZ": "America","CA": "America","CC": "Asia","CD": "Africa","CF": "Africa","CG": "Africa","CH": "Europe","CI": "Africa","CK": "Oceania","CL": "America","CM": "Africa","CN": "Asia","CO": "America","CR": "America","CU": "America","CV": "Africa","CX": "Asia","CY": "Asia","CZ": "Europe","DE": "Europe","DJ": "Africa","DK": "Europe","DM": "America","DO": "America","DZ": "Africa","EC": "America","EE": "Europe","EG": "Africa","EH": "Africa","ER": "Africa","ES": "Europe","ET": "Africa","FI": "Europe","FJ": "Oceania","FK": "America","FM": "Oceania","FO": "Europe","FR": "Europe","GA": "Africa","GB": "Europe","GD": "America","GE": "Asia","GF": "America","GG": "Europe","GH": "Africa","GI": "Europe","GL": "America","GM": "Africa","GN": "Africa","GP": "America","GQ": "Africa","GR": "Europe","GS": "Antarctica","GT": "America","GU": "Oceania","GW": "Africa","GY": "America","HK": "Asia","HN": "America","HR": "Europe","HT": "America","HU": "Europe","ID": "Asia","IE": "Europe","IL": "Asia","IM": "Europe","IN": "Asia","IO": "Asia","IQ": "Asia","IR": "Asia","IS": "Europe","IT": "Europe","JE": "Europe","JM": "America","JO": "Asia","JP": "Asia","KE": "Africa","KG": "Asia","KH": "Asia","KI": "Oceania","KM": "Africa","KN": "America","KP": "Asia","KR": "Asia","KW": "Asia","KY": "America","KZ": "Asia","LA": "Asia","LB": "Asia","LC": "America","LI": "Europe","LK": "Asia","LR": "Africa","LS": "Africa","LT": "Europe","LU": "Europe","LV": "Europe","LY": "Africa","MA": "Africa","MC": "Europe","MD": "Europe","ME": "Europe","MG": "Africa","MH": "Oceania","MK": "Europe","ML": "Africa","MM": "Asia","MN": "Asia","MO": "Asia","MP": "Oceania","MQ": "America","MR": "Africa","MS": "America","MT": "Europe","MU": "Africa","MV": "Asia","MW": "Africa","MX": "America","MY": "Asia","MZ": "Africa","NA": "Africa","NC": "Oceania","NE": "Africa","NF": "Oceania","NG": "Africa","NI": "America","NL": "Europe","NO": "Europe","NP": "Asia","NR": "Oceania","NU": "Oceania","NZ": "Oceania","OM": "Asia","PA": "America","PE": "America","PF": "Oceania","PG": "Oceania","PH": "Asia","PK": "Asia","PL": "Europe","PM": "America","PN": "Oceania","PR": "America","PS": "Asia","PT": "Europe","PW": "Oceania","PY": "America","QA": "Asia","RE": "Africa","RO": "Europe","RS": "Europe","RU": "Europe","RW": "Africa","SA": "Asia","SB": "Oceania","SC": "Africa","SD": "Africa","SE": "Europe","SG": "Asia","SH": "Africa","SI": "Europe","SJ": "Europe","SK": "Europe","SL": "Africa","SM": "Europe","SN": "Africa","SO": "Africa","SR": "America","ST": "Africa","SV": "America","SY": "Asia","SZ": "Africa","TC": "America","TD": "Africa","TF": "Antarctica","TG": "Africa","TH": "Asia","TJ": "Asia","TK": "Oceania","TM": "Asia","TN": "Africa","TO": "Oceania","TR": "Asia","TT": "America","TV": "Oceania","TW": "Asia","TZ": "Africa","UA": "Europe","UG": "Africa","US": "America","UY": "America","UZ": "Asia","VC": "America","VE": "America","VG": "America","VI": "America","VN": "Asia","VU": "Oceania","WF": "Oceania","WS": "Oceania","YE": "Asia","YT": "Africa","ZA": "Africa","ZM": "Africa","ZW": "Africa"}
GEOIPURL = "http://www.freegeoip.net/json/"
TIMEOUT = 3
TTL = 32

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
        ans,unans = sr(packet, verbose=0, timeout=TIMEOUT)
        try:
            sent = datetime.fromtimestamp(ans[0][0].sent_time)
            recived = datetime.fromtimestamp(ans[0][1].time)
            rtt = (recived - sent).total_seconds() * 1000
            if ans[0][1].sprintf('%type%') == '11':
                r = ans[0][1].sprintf('%src%')
                routers.append((r,float(rtt)))
            if ans[0][1].sprintf('%type%') == '0':
                r = ans[0][1].sprintf('%src%')
                routers.append((r,float(rtt)))
                llegue = True        
        except:
            routers.append(('null','null'))

    return routers, llegue

#input [(router_ip,rtt)]
#return router_ip, rtt
def sacar_host_mediana(list_of_host):
    sin_null = []
    for i in list_of_host:
        if i[0] != 'null':
            sin_null.append(i)
    if sin_null == []:
        return ('null','null')
    sin_null.sort(key=lambda tup: tup[1])
    median_index = len(list_of_host)/2
    return sin_null[median_index][0], sin_null[median_index][1]





def calcularT(x):
    y = {
        3: 1.1511,
        4: 1.4250,
        5: 1.5712,
        6: 1.6563,
        7: 1.7110,
        8: 1.7491,
        9: 1.7770,
        10: 1.7984,
        11: 1.8153,
        12: 1.8290,
        13: 1.8403,
        14: 1.8498,
        15: 1.8579,
        16: 1.8649,
        17: 1.8710,
        18: 1.8764,
        19: 1.8811,
        20: 1.8853,
        21: 1.8891,
        22: 1.8926,
        23: 1.8957,
        24: 1.8985,
        25: 1.9011,
        26: 1.9035,
        27: 1.9057,
        28: 1.9078,
        29: 1.9096,
        30: 1.9114,
        31: 1.9130,
        32: 1.9146,
        33: 1.9160,
        34: 1.9174,
        35: 1.9186,
        36: 1.9198,
        37: 1.9209,
        38: 1.9220,
    }
    try:
        return y[x]
    except:
        if (39 <= x <= 50):
            return 1.9314
        if (51 <= x <= 100):
            return 1.9459
        if (101 <= x <= 1000):
            return 1.9586
    return 1.9600


def removeOutliersAux(aux1):
    #sacamos los que son null
    aux = []
    for i in aux1:
        if i != 'null':
            aux.append(i)
    aux.sort()
    if aux != []:
        outliers = []
        while(True):
            size = len(aux)
            promedio = sum(aux)/size
            desvio = numpy.std(aux)
            t = calcularT(size)
            desvio_1 = abs(aux[0] - promedio)
            desvio_n = abs(aux[-1] - promedio)
            maximo = max(desvio_1, desvio_n)
            if(maximo == desvio_1):
                if(t*desvio < maximo):
                    outliers.append(aux.pop(0))
                else:
                    break
            if(maximo == desvio_n):
                if(t*desvio < maximo):
                    outliers.append(aux.pop(size-1))
                else:
                    break
        return aux,outliers
    else:
        return aux1,aux1

def continent_of_ip(router_ip):
    try:
        req = requests.get(GEOIPURL+router_ip,timeout=5)
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


def what_continent_belong(list_of_host):
    list_of_host[0].salto_intercontinental_by_api = 'false'
    for indice in range(1,len(list_of_host)):
        list_of_host[indice].continent = continent_of_ip(list_of_host[indice].ip_address)
        if list_of_host[indice-1].continent == 'null' or list_of_host[indice].continent == 'null':
            list_of_host[indice].is_intercontinental = 'null'    
        else:
            list_of_host[indice].salto_intercontinental_by_api = str(list_of_host[indice-1].continent != list_of_host[indice].continent)

def traceroute(dest,rafaga,checkeiarConGeoIP):
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
    for ttl in range(1,TTL):
        host_rafaga, llegue = routers_in_specific_ttl(dest,ttl,rafaga)
        hop_ip,rtt = sacar_host_mediana(host_rafaga)
        router_temp = Router(hop_ip,rtt,ttl)
        list_of_host.append(router_temp)
        if llegue:
            break
    # So here I have my list of routers in each ttl iteration
    # then we need to know which continent belongs
    if checkeiarConGeoIP:
        what_continent_belong(list_of_host)
        list_para_json = []
        for i in range(len(list_of_host)):
            dicc_para_json={"rtt":list_of_host[i].rtt, "ip_address":list_of_host[i].ip_address, "salto_intercontinental":list_of_host[i].salto_intercontinental, "hop_number":list_of_host[i].hop_num, "continent": list_of_host[i].continent}
            list_para_json.append(dicc_para_json)
    else:
        rtts = []
        for l in list_of_host:
            rtts.append(l.rtt)
        normales, outliers = removeOutliersAux(rtts)

        list_para_json = []
        for i in range(len(list_of_host)):
            if list_of_host[i].rtt != 'null':
                salto =  list_of_host[i].rtt in outliers
            else:
                salto = 'null'
            dicc_para_json={"rtt":list_of_host[i].rtt, "ip_address":list_of_host[i].ip_address, "salto_intercontinental":salto, "hop_number":list_of_host[i].hop_num}
            list_para_json.append(dicc_para_json)

    print json.dumps(list_para_json, indent=2)
 
if __name__ == '__main__':
    arg = sys.argv[1:]
    dest = arg[0]
    rafaga = int(arg[1])
    con_geo_ip = int(arg[2])
    traceroute(dest,rafaga,con_geo_ip)
