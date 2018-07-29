import ipaddress
import re
import requests
from datetime import date
from dateutil.parser import parse as date_parse

# Calculates number of months
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

# Generate data set by extracting the features from the URL
def generate_data_set(url):

    data_set = []

    # Converts the given URL into standard format
    if not re.match(r"^https?", url):
        url = "http://" + url

    print("CHECKING FOR "+url)

    # Stores the response of the given URL
    try:
        response = requests.get(url)
    except:
        response = ""

    # Extracts domain from the given URL
    domain = re.findall(r"://([^/]+)/?", url)[0]

    # Requests all the information about the domain
    whois_response = requests.get("https://www.whois.com/whois/"+domain)

    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })


    # Extracts global rank of the website
    try:
        global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        global_rank = -1

    print("RANK = "+str(global_rank))

    # having_IP_Address
    try:
        ipaddress.ip_address(url)
        data_set.append(1)
    except:
        data_set.append(-1)

    # URL_Length
    if len(url) < 54:
        data_set.append(1)
    elif len(url) >= 54 and len(url) <= 75:
        data_set.append(0)
    else:
        data_set.append(-1)

    # Shortining_Service
    if re.findall("goo.gl|bit.ly", url):
        data_set.append(1)
    else:
        data_set.append(-1)

    # having_At_Symbol
    if re.findall("@", url):
        data_set.append(1)
    else:
        data_set.append(-1)

    # double_slash_redirecting
    if re.findall(r"[^https?:]//",url):
        data_set.append(-1)
    else:
        data_set.append(1)

    # Prefix_Suffix
    if re.findall(r"https?://[^\-]+-[^\-]+/", url):
        data_set.append(-1)
    else:
        data_set.append(1)

    # having_Sub_Domain
    if len(re.findall("\.", url)) == 1:
        data_set.append(-1)
    elif len(re.findall("\.", url)) == 2:
        data_set.append(0)
    else:
        data_set.append(1)

    # SSLfinal_State
    data_set.append(0)

    # Domain_registeration_length
    data_set.append(0)

    # Favicon
    data_set.append(0)

    # port
    try:
        port = domain.split(":")[1]
        if port:
            data_set.append(1)
        else:
            data_set.append(-1)
    except:
        data_set.append(-1)

    # HTTPS_token
    if re.findall("^https\-", domain):
        data_set.append(-1)
    else:
        data_set.append(1)

    # Request_URL
    data_set.append(0)

    # URL_of_Anchor
    data_set.append(0)

    # Links_in_tags
    data_set.append(0)

    # SFH
    data_set.append(0)

    # Submitting_to_email
    if re.findall(r"[mail\(\)|mailto:?]", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # Abnormal_URL
    if response.text == "":
        data_set.append(1)
    else:
        data_set.append(-1)

    # Redirect
    if len(response.history) <= 1:
        data_set.append(-1)
    elif len(response.history) <= 4:
        data_set.append(0)
    else:
        data_set.append(1)

    # on_mouseover
    if re.findall("<script>.+onmouseover.+</script>", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # RightClick
    if re.findall(r"event.button ?== ?2", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # popUpWidnow
    if re.findall(r"alert\(", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # Iframe
    if re.findall(r"[<iframe>|<frameBorder>]", response.text):
        data_set.append(1)
    else:
        data_set.append(-1)

    # age_of_domain
    try:
        registration_date = re.findall(r'Registration Date:</div><div class="df-value">([^<]+)</div>', whois_response.text)[0]
        print("AGE OF DOMAIN = "+str(registration_date))

        if diff_month(date.today(), date_parse(registration_date)) >= 6:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)


    # DNSRecord
    data_set.append(0)

    # web_traffic
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # Page_Rank
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # Google_Index
    try:
        if global_rank > 0 and global_rank < 100000:
            data_set.append(-1)
        else:
            data_set.append(1)
    except:
        data_set.append(1)

    # Links_pointing_to_page
    number_of_links = len(re.findall(r"<a href=", response.text))
    if number_of_links == 0:
        data_set.append(1)
    elif number_of_links <= 2:
        data_set.append(0)
    else:
        data_set.append(-1)

    # Statistical_report
    data_set.append(0)

    print data_set

    print "- HAVING IP ADDRESS = "+str(data_set[0])
    print "- URL LENGTH = "+str(data_set[1])
    print "- SHORTINING SERVICE = "+str(data_set[2])
    print "- DOUBLE SLASH REDIRECTING = "+str(data_set[3])
    print "- PREFIX SUFFIX = "+str(data_set[4])
    print "- HAVING SUB DOMAIN = "+str(data_set[5])
    print "- SSL FINAL STATE = "+str(data_set[6])
    print "- DOMAIN REGISTRATION LENGHT = "+str(data_set[7])
    print "- FAVICON = "+str(data_set[8])
    print "- PORT = "+str(data_set[10])
    print "- HTTPS TOKEN = "+str(data_set[11])
    print "- REQUEST URL = "+str(data_set[12])
    print "- URL OF ANCHOR = "+str(data_set[13])
    print "- LINKS IN TAGS = "+str(data_set[15])
    print "- SFH = "+str(data_set[16])
    print "- ABNORMAL URL = "+str(data_set[17])
    print "- REDIRECT = "+str(data_set[18])
    print "- ON MOUSE OVER = "+str(data_set[19])
    print "- RIGHT CLICK = "+str(data_set[20])
    print "- POPUP WINDOW = "+str(data_set[21])
    print "- IFRAME = "+str(data_set[22])
    print "- AGE OF DOMAIN = "+str(data_set[23])
    print "- DNS RECORD = "+str(data_set[24])
    print "- WEB TRAFFIC = "+str(data_set[25])
    print "- PAGE RANK = "+str(data_set[26])
    print "- GOOGLE INDEX = "+str(data_set[27])
    print "- LINK POINTING TO PAGE = "+str(data_set[28])
    print "- STATISTICAL REPORT = "+str(data_set[29])

    return data_set
