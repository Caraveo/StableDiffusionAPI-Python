import sys
import os
import random
import json
import time
from urllib.parse import urlparse
from urllib.parse import quote
import urllib.parse
import http.client
from StableDiffusionAPI import key as key
import threading

class console_colors:
    HEADER = '\033[95m'
    OK = '\033[94m'
    OKCYAN = '\033[96m'
    SUCCESES = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def Text2Img(query2, width, height, name):
    try:
        thread = threading.Thread(target=Text2Img_Threader, args=(query2, width, height, name))
        thread.start()
        print(f"{console_colors().SUCCESES}{name}: Successfully Started as Thread{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: Failed to start as Thread{console_colors.ENDC}")


def Text2Img_Threader(query2, width, height, name):
    query = quote(query2)
    img = name
    conn = http.client.HTTPSConnection("stablediffusionapi.com")
    payload = ''

    if width <= 512:
        width = 512
    elif width >= 1024:
        width = 1024
    else:
        check_width = width.to_bytes(10, byteorder='big')
    check_width = width.to_bytes(10, byteorder='big')
    
    if height <= 512:
        height = 512
    elif height >= 1024:
        height = 1024
    else:
        check_height = height.to_bytes(10, byteorder='big')
    check_height = height.to_bytes(10, byteorder='big')

    try:
        quote(check_height)
        quote(check_width)
        print(f"{console_colors().SUCCESES}{name}: Height and Width are valid{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: Height and Width are invalid{console_colors.ENDC}")
        exit()

    try:
        key
        # print(f"{console_colors().SUCCESES}{name} Key Set{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: No Key Error: No value detected, Set a key with{console_colors.ENDC} {console_colors().OKCYAN}SetKey(){console_colors.ENDC}")
        exit()

    string_height_int = str(height)
    string_width_int = str(width)

    #print(string_height_int)
    #print(string_width_int)
    
    headers = {
    'key': key.value
    }
    uriPrompt = str("/api/v3/text2img?prompt=" + query + "&width=" + string_width_int + "&height="+ string_height_int +"&samples=1")
    
    #print(uriPrompt)
    conn.request("POST", uriPrompt, payload, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data)

    jrespone = json.loads(data)

    if jrespone["output"]:
        #print(jrespone["output"])
        url = jrespone["output"]
        urlHost = url[0]
      
        uri = urlHost
        #print(urlHost)
        parsed = urlparse(uri)
        #print(parsed)

        base = parsed.netloc
        #print(base)

        path = parsed.path
        #print(path)

        with_path = base + '/'.join(path.split('/')[:-1])
        #print(with_path)

        #print(path.split('/')) 

        conn.close()

        download_img_Threader(base, path, name)
    else:
        print(f"{console_colors().FAIL}{name}: No results{console_colors.ENDC}")
        timetotry = jrespone["eta"]
        print(f"{console_colors().OK}{name}: Trying in: {timetotry}{console_colors.ENDC}")
        time.sleep(timetotry)
        conn.close()
        conn.request("POST", jrespone["fetch_result"], payload, headers)
        fetchResponse = conn.getresponse()
        fetchData = fetchResponse.read()
        jFetchData = json.loads(fetchData)
        jFetch = jFetchData["output"]
        #print(jFetch)

        parsed = urlparse(jFetch[0])
        #print(parsed)

        base = parsed.netloc
        #print(base)

        path = parsed.path
        #print(path)

        with_path = base + '/'.join(path.split('/')[:-1])
        #print(with_path)
        #print(path.split('/')) 

        conn.close()

        download_img_Threader(base, path, name)
    conn.close()


def download_img_Threader(base, path, name):
    try:
        thread = threading.Thread(target=download_img, args=(base, path, name))
        thread.start()
        print(f"{console_colors().SUCCESES}{name}: Successfully Started Download Thread{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: Failed to start Download Thread{console_colors.ENDC}")

def download_img(base, path, name):
    time.sleep(1)
    img = name
    conn = http.client.HTTPSConnection(base)
    payload = ''
    headers = {}
    conn.request("GET", path, payload, headers)
    res = conn.getresponse()
    data = res.read()
    if res.status == 200:
        with open(img, "wb") as f:
            f.write(data)
            print(f"{console_colors().SUCCESES}{name}: Image downloaded successfully! {console_colors.ENDC}")
    else:
        print(f"{console_colors().FAIL}{name}: Fetch2 Error downloading image: {res.status} {res.reason} {console_colors.ENDC}")
    conn.close()