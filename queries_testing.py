import os
import requests
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

queries_df = pd.read_csv(os.path.join("data", "bss_queries_day.csv"), sep="\t")


url_srv = os.getenv("SERVICE_URL")
url_kuber = os.getenv("SERVICE_URL_KUBER")

test_results = []
for i, d in enumerate(queries_df.to_dict(orient="records")[:100]):
    query ={
        "pubid": 9,
        "chat_id": 0,
        "userid": 0,
        "text": d["Query"]
        }

    try:
        t0 = time.time()
        search_result = requests.post(url_kuber, json=query)
        t1 = time.time()
        s_d = search_result.json()
        test_results.append({**d, **s_d, **{"timeout": t1 - t0}})
        print(i, "timeout:", t1 - t0)
    except:
        print("Error")

timeouts_df = pd.DataFrame(test_results)
print(timeouts_df)

timeouts_df.to_csv(os.path.join("data", "test_results.csv"), sep="\t", index=False)