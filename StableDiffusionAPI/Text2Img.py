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

def Text2Img(query2, width, height, name):
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
        print("Height and Width are valid")
    except:
        print("Height and Width are invalid")
        exit()

    try:
        key
        print("Key Set")
        print(key)
    except:
        print("No Key Error: No value detected, Set a key with SetKey()")
        exit()


    #convert bytes to int
    string_height_int = str(height)
    string_width_int = str(width)

    print(string_height_int)
    print(string_width_int)
    
    headers = {
    'key': key.value
    }
    uriPrompt = str("/api/v3/text2img?prompt=" + query + "&width=" + string_width_int + "&height="+ string_height_int +"&samples=1")
    
    print(uriPrompt)
    conn.request("POST", uriPrompt, payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

    jrespone = json.loads(data)

    if jrespone["output"]:
        print(jrespone["output"])
        url = jrespone["output"]
        urlHost = url[0]
        uri = urlHost
        print (urlHost)

        parsed = urlparse(uri)

        print(parsed)

        base = parsed.netloc
        print(base)

        path = parsed.path
        print(path)

        with_path = base + '/'.join(path.split('/')[:-1])
        print(with_path)

        print(path.split('/')) 

        conn.close()

        conn = http.client.HTTPSConnection(base)
        payload = ''
        headers = {}
        conn.request("GET", path, headers)
        res = conn.getresponse()
        data = res.read()

        if res.status == 200:
            with open(img, "wb") as f:
                f.write(data)
                print("Image downloaded successfully!")
        else:
            print(f"Error downloading image: {response.status} {response.reason}")
        conn.close()
    else:
        print("No results")
        print(jrespone["fetch_result"])
        timetotry = jrespone["eta"]
        print("Trying in: ", timetotry)
        time.sleep(timetotry)
        conn.close()
        conn.request("POST", jrespone["fetch_result"], payload, headers)
        fetchResponse = conn.getresponse()
        fetchData = fetchResponse.read()

        jFetchData = json.loads(fetchData)

        jFetch = jFetchData["output"]

        print(jFetch)

        parsed = urlparse(jFetch[0])

        print(parsed)

        base = parsed.netloc
        print(base)

        path = parsed.path
        print(path)

        with_path = base + '/'.join(path.split('/')[:-1])
        print(with_path)

        print(path.split('/')) 

        conn.close()

        conn = http.client.HTTPSConnection(base)
        payload = ''
        headers = {}
        conn.request("GET", path, payload, headers)
        res = conn.getresponse()
        data = res.read()


        if res.status == 200:
            with open(img, "wb") as f:
                f.write(data)
                print("Image downloaded successfully!")
        else:
            print(f"Error downloading image: {response.status} {response.reason}")
        conn.close()
    conn.close()
