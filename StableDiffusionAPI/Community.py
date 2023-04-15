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

tries = 3

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

def Text2Img(model, prompt, name):
    try:
        width = 512
        height = 512
        thread = threading.Thread(target=Text2Img_Threader, args=(model, prompt, width, height, name))
        thread.start()
        print(f"{console_colors().SUCCESES}{name}: Successfully Started as Thread{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: Failed to start as Thread{console_colors.ENDC}")


def Text2Img_Threader(modeler, query, width, height, name):
    try:
        mod = quote(modeler)
        print(f"{console_colors().SUCCESES}{name}: Successfully Verified {mod} Model{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: Failed to Verify {mod}{console_colors.ENDC}")


    query = quote(query)
    img = name


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
    try:
        key
        # print(f"{console_colors().SUCCESES}{name} Key Set{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: No Key Error: No value detected, Set a key with{console_colors.ENDC} {console_colors().OKCYAN}SetKey(){console_colors.ENDC}")


    string_height_int = str(height)
    string_width_int = str(width)

    try: 
        conn = http.client.HTTPSConnection("stablediffusionapi.com")
        payload = ''
        headers = {'key': key.value}
        uriPrompt = str("/api/v3/dreambooth?model_id=" + mod + "&prompt=" + query + "&width=512&height=512&samples=1")
        conn.request("POST", uriPrompt, payload, headers)
        res = conn.getresponse()
        data = res.read()
        jresponse = json.loads(data)
        result = jresponse["status"]
        conn.close()

        if result == "failed":
            print(f"{console_colors().FAIL}{name}: Status: {result}{console_colors.ENDC}")
            conn.close()

        elif result == "success": 
            print(f"{console_colors().OK}{name}: Status: {result}{console_colors.ENDC}")
            connection_generator(jresponse, res, name, headers, payload)
        elif result == "processing":
            print(f"{console_colors().OK}{name}: Status: {result}{console_colors.ENDC}")
            connection_generator(jresponse, res, name, headers, payload)
        else:
            print(f"{console_colors().FAIL}{name}: Status: {result}{console_colors.ENDC}")
            conn.close()

    except:
        print(f"{console_colors().FAIL}{name}: Response: {res.status} {res.reason}{console_colors.ENDC}")


    

def connection_generator(jsonResponse, res, name, header, payload):
    try:
        attempt = 0
        while jsonResponse["status"] == "processing" and attempt < tries or jsonResponse["status"] == "success" and attempt < tries:
            if jsonResponse["status"] == "processing":
                eta_time = jsonResponse["eta"]
                timer = eta_time
                print(f"{console_colors().OK}{name}: ETA: {jsonResponse['eta']}{console_colors.ENDC}")
                time.sleep(eta_time)
                try:
                    fetch_result = jsonResponse["fetch_result"]
                    print(fetch_result)
                    jsonResponse = fetch_result(fetch_result, name, header, payload)
                    print(jsonResponse)
                    parsed_base = fetch_result_parser(fetch_result)["base"]
                    parsed_path = fetch_result_parser(fetch_result)["path"]
                except:
                    print(f"{console_colors().OKCYAN}{name}: Could Not Fetch: {res.status} {res.reason}{console_colors.ENDC}")
                    pass
            elif jsonResponse["status"] == "success" and attempt == 0:
                try:
                    gen_time = jsonResponse["generationTime"]
                    timer = gen_time
                    print(f"{console_colors().OK}{name}: Generation Time: {jsonResponse['generationTime']}{console_colors.ENDC}")
                    time.sleep(gen_time)
                    output_result = jsonResponse["output"]
                    parsed_base = output_result_parser(output_result[0])["base"]
                    parsed_path = output_result_parser(output_result[0])["path"]
                    try:
                        download_img_Threader(parsed_base, parsed_path, name, gen_time)
                    except:
                        print(f"{console_colors().FAIL}{name}: Failed to start Threader{console_colors.ENDC}")

                    break
                except:
                    print(f"{console_colors().FAIL}{name}: Download Result Failed: {jsonResponse['output']}{console_colors.ENDC}")
                    conn.close()
            else:
                download_img_Threader(base, path, name, timer)

            print(f"{console_colors().OK}{name}: Fetch Attempt: {attempt + 1 }{console_colors.ENDC}")
            attempt += 1
        if attempt > tries:
            print(f"{console_colors().FAIL}{name}: Max Attempts Reached{console_colors.ENDC}")
            conn.close()
    except:
        print(f"{console_colors().FAIL}{name}: Download Connection Error: {res.status} {res.reason}{console_colors.ENDC}")
        conn.close()

def fetch_result(fetch_result, name, headers, payload):
    try:
        conn.close()
        fetch_result_parser(fetch_result)
        parsed_base = fetch_result_parser(fetch_result)["base"]
        print(parsed_base)
        parsed_path = fetch_result_parser(fetch_result)["path"]
        conn = http.client.HTTPSConnection(parsed_base)
        conn.request("GET", parsed_path, payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data)
        if res.status == 200:
            dataJson = json.loads(data)
            print(dataJson)
            try:
                conn.close()
                return dataJson
            except:
                print(f"{console_colors().FAIL}{name}: Fatal Error: {dataJson}{console_colors.ENDC}")
                conn.close()
    except:
        print(f"{console_colors().FAIL}{name}: Fetching Failed: {res.status} {res.reason}{console_colors.ENDC}")
        conn.close()

def fetch_result_parser(fetch_result):
    parsed_base = urlparse(fetch_result).netloc
    parsed_path = urlparse(fetch_result).path
    return {"base": parsed_base, "path": parsed_path}


def output_result_parser(output_result):
    parsed_base = urlparse(output_result).netloc
    parsed_path = urlparse(output_result).path
    return {"base": parsed_base, "path": parsed_path}
    
 

def download_img_Threader(base, path, name, timer):
    try:
        thread = threading.Thread(target=download_img, args=(base, path, name, timer))
        thread.start()
        print(f"{console_colors().SUCCESES}{name}: Successfully Started Download Thread{console_colors.ENDC}")
    except:
        print(f"{console_colors().FAIL}{name}: Failed to start Download Thread{console_colors.ENDC}")

def download_img(base, path, name, timer):
    try:
        time.sleep(timer)
        conn = http.client.HTTPSConnection(base)
        payload = ''
        headers = {}
        conn.request("GET", path, payload, headers)
        res = conn.getresponse()
        data = res.read()
        if res.status == 200:
            with open(name, "wb") as f:
                f.write(data)
                print(f"{console_colors().SUCCESES}{name}: Image downloaded successfully! {console_colors.ENDC}")
        else:
            print(f"{console_colors().FAIL}{name}: Fatal Error downloading image: {res.status} {res.reason} {console_colors.ENDC}")
        conn.close()
    except:
        print(f"{console_colors().FAIL}{name}: Image Download Connection Error: {res.status} {res.reason}{console_colors.ENDC}")
        conn.close()