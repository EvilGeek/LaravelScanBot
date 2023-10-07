import ipaddress, random, requests, urllib3, re
urllib3.disable_warnings()


def generate_ipv4():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

def generate_ipv6():
    ipv6 = ipaddress.IPv6Address(random.randint(0, 2**128 - 1))
    return str(ipv6)

def extract_ipv4(string):
    return list(set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', string)))

def extract_ipv6(string):
    ipv6_pattern = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4})|(([0-9a-fA-F]{1,4}:){1,7}:)|(([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4})|(([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2})|(([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3})|(([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4})|(([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5})|([0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})?)|(:((:[0-9a-fA-F]{1,4}){1,7})?)'
    ipv6_addresses = re.findall(ipv6_pattern, string)
    extracted_ipv6 = [match[0] for match in ipv6_addresses if match[0] != '']
    return extracted_ipv6

def extract_ips(string):
    ipv4_addresses = extract_ipv4(string)
    ipv6_addresses = extract_ipv6(string)
    return ipv4_addresses + ipv6_addresses

def extract_domains(string):
    domain_pattern = r'(?<=https://|http://|www\.|ftp://)([A-Za-z0-9.-]+)(?=[^\w]|$)'
    subdomain_pattern = r'(?<=https://|http://|ftp://)([A-Za-z0-9.-]+)(?=[^\w]|$)'
    
    domains = re.findall(domain_pattern, string)
    subdomains = re.findall(subdomain_pattern, string)
    
    combined_domains = domains + subdomains
    
    return list(set(combined_domains))

def extract_all_ip_domain(string):

    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv6_pattern = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4})|(([0-9a-fA-F]{1,4}:){1,7}:)|(([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4})|(([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2})|(([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3})|(([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4})|(([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5})|([0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})?)|(:((:[0-9a-fA-F]{1,4}){1,7})?)'
    domain_pattern = r'(?<=https://|http://|www\.|ftp://)([A-Za-z0-9.-]+)(?=[^\w]|$)'
    subdomain_pattern = r'(?<=https://|http://|ftp://)([A-Za-z0-9.-]+)(?=[^\w]|$)'

    ipv4_addresses = re.findall(ipv4_pattern, string)
    ipv6_addresses = re.findall(ipv6_pattern, string)
    domains = re.findall(domain_pattern, string)
    subdomains = re.findall(subdomain_pattern, string)

    return ipv4_addresses + ipv6_addresses + domains + subdomains



def ip_information(ip):
    
    url = "http://ipapi.co/"+ip+"/json/"
    headers = {
       "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57",
       "accept": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, verify=False)
        if r.json().get("error"):
            return {
              "error": r.json().get("reason", "Unknown")
            }
        return r.json()
    except Exception as e:
        return {
          "error": "Internal Server Error: "+str(e)
        }


def random_domain_name(word_list, extensions, l=2):
    return "".join([random.choice(word_list) for _ in range(random.randint(1, l))]) + random.choice(extensions)


def find_cidr(html):
    regex=r'(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?'
    return re.findall(regex,html)

def AsnToCidr(asn):
    h={
    "sec-ch-ua": "\"Not?A_Brand\";v\u003d\"8\", \"Chromium\";v\u003d\"108\", \"Google Chrome\";v\u003d\"108\"",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
    "content-type": "application/json; charset\u003dutf-8",
    "accept": "application/json, text/javascript, */*; q\u003d0.01",
    "tempauthorization": "27eea1cd-e644-4b7b-bebe-38010f55dab3",
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": f"https://mxtoolbox.com/SuperTool.aspx?action\u003dasn%3a{asn}\u0026run\u003dtoolpage",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7",
    "cookie": "__hssc\u003d179393531.5.1673980640179"
    }
    req=requests.get(f"https://mxtoolbox.com/api/v1/Lookup?command\u003dasn\u0026argument\u003das{asn}\u0026resultIndex\u003d2\u0026disableRhsbl\u003dtrue\u0026format\u003d2", headers=h, verify=False).json()
    return str(req["HTML_Value"])


def is_valid_asn(asn):
    try:
        asn = int(asn)
        return 1 <= asn <= 65535 or 4200000000 <= asn <= 4294967295
    except ValueError:
        return False

def asn_to_cidr(asn):
    try:
        x = AsnToCidr(asn)
        print(x)
        return find_cidr(x)
    except Exception as e:
        print(e)
        return []

def find_asn(text):
    return re.findall(r'\d{1,10}', text)

def cidr_to_ip(cidr):
    try:
        iplist=[]
        for ip in ipaddress.IPv4Network(cidr):
            iplist.append(str(ip))
        return iplist
    except Exception as e:
        return []
