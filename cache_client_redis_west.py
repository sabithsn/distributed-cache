import requests
import json
import time

# request_type = "database"
request_type = "static"

if request_type == "database":

    misses = 0
    start_time = time.time()

    titles = []
    with open ("sample.txt", "r") as f:
        for line in f:
            titles.append(line.strip())

    for i in range (100):

        title = titles[i]
        data = {
            'title': title
        }

        response = requests.post('http://34.102.46.81:6666/db_query/', data=data)
        rcvd_data = response.json()

        if response.status_code == 200:
            misses += rcvd_data["miss"]

            # print('POST request successful!')
            # print ("rcvd_data:", rcvd_data)
        else:
            print('POST request failed!')

    end_time = time.time()

    print ("time taken:", end_time-start_time)
    print ("cache hits:", 100-misses)
    print ("cache misses:", misses)

else:

    misses = 0
    start_time = time.time()

    for i in range (100):
        response = requests.post('http://34.102.46.81:6666/')
        rcvd_data = response.json()

        if response.status_code == 200:
            misses += rcvd_data["miss"]

            # print('POST request successful!')
            # print ("rcvd_data:", rcvd_data)
        else:
            print('POST request failed!')

    end_time = time.time()

    print ("time taken:", end_time-start_time)
    print ("cache hits:", 100-misses)
    print ("cache misses:", misses)