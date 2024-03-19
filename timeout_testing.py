import os
import requests
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

query ={
  "pubid": 9,
  "chat_id": 0,
  "userid": 0,
  "text": "может ли ООО сдавать упрощенный баланс?"
}

url_srv = os.getenv("SERVICE_URL")
url_kuber = os.getenv("SERVICE_URL_KUBER")

s = 0
timeouts = []
for i in range(100):
    try:
        t0 = time.time()
        res = requests.post(url_kuber, json=query)
        t1 = time.time()
        timeouts.append({"timeout:": t1 - t0})
        s += t1 - t0
        print(i + 1, res.json())
        print("timeout:", t1 - t0)
        print(i + 1, "average timeout:", s/(i + 1))
    except:
        timeouts.append({"timeout:": "Error"})
        print("Error")

timeouts_df = pd.DataFrame(timeouts)
print(timeouts_df)
timeouts_df.to_csv(os.path.join("data", "timeouts_kuber.csv"), sep="\t", index=False)