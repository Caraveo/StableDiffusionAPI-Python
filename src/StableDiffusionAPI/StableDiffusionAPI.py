import sys
import os
import random
import json
import time
from urllib.parse import urlparse
import urllib.parse
import http.client

def StableDiffusionAPI(query2, width, height, samples, name):
    query = urllib.parse.quote(query2)
    img = name
    conn = http.client.HTTPSConnection("stablediffusionapi.com")
    payload = ''
    headers = {
    'key': 'XXXXXXXXXX'
    }
    uriPrompt = str("/api/v3/text2img?prompt=" + query + "&width=512&height=512&samples=1")
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
