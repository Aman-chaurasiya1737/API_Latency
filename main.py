import requests
import numpy as np
import pandas as pd
from datetime import datetime
import time
import matplotlib.pyplot as plt
df = pd.DataFrame(columns=["API name","timestamp","latency","status code"])
i = 0

def test_api(api_name, endpoint, payload=None,iteration=1):
    global i,p95,p99
    for _ in range(iteration):
        try:
            response = requests.get(endpoint, params=payload)
            latency = response.elapsed.total_seconds()
            current_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            if response.status_code == 200:
                df.loc[i] = [api_name, current_timestamp, latency, response.status_code]
                # print(response.json())   #shows the data 
                
            else:
                df.loc[i] = [api_name, current_timestamp, latency, response.status_code]

        except Exception as e:
            current_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            df.loc[i] = [api_name, current_timestamp, 0, "error"]
            print(f"{api_name} error: {e}")
        time.sleep(2)
        i += 1
    p95=np.percentile(df[df["API name"]==api_name]["latency"],95)
    p99=np.percentile(df[df["API name"]==api_name]["latency"],99)
    print(f"for {api_name} p95 is {p95} seconds ")
    print(f"for {api_name} p99 is {p99} seconds")
    plt.plot(df[df["API name"]==api_name]["timestamp"],df[df["API name"]==api_name]["latency"])
    plt.ylabel("Latency")
    plt.xlabel("timestamp")
    plt.title("Latency line chart")
    plt.show()
    # print(df[df["API name"]==api_name]["latency"].mean())


api_name=input("enter the API Name\n\n")
api_key=input("Enter the API URL endpoint\n")
payload={}
para=input("Enter \"yes\" if you want to pass any parameter else Enter \"no\"\n")
if para.strip().lower()=="yes":
    no_of_para=int(input("Enter the no. of parameters\n"))
    for _ in range(no_of_para):
        type_of_para=input("enter the type of parameter\n")
        actual_para=input("Enter the parameter\n")
        payload.update({type_of_para:actual_para})
iteration=int(input("enter the no. of iteration that how many times your key to be tested\n"))





test_api(api_name,api_key, payload,iteration)
# test_api("nationalize", "https://api.nationalize.io", {"name":"Aman"})
# test_api("ipify", "https://api.ipify.org?format=json")
# test_api("jokes", "https://official-joke-api.appspot.com/random_joke")
# test_api("zippopotam", "https://api.zippopotam.us/us/33162")



df.to_csv("output.csv", index=False)
# print(df)