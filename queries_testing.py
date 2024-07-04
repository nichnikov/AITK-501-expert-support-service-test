import os
import requests
import time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

queries_df = pd.read_csv(os.path.join("data", "AITK552_bss_supp_queries.csv"), sep="\t")

# "Query	ShortQuery"

url_srv = os.getenv("SERVICE_URL_SRV")
url_kuber = os.getenv("SERVICE_URL_KUBER")
url_balance = os.getenv("SERVICE_URL_BALANCE")
test_results = []
for i, d in enumerate(queries_df.to_dict(orient="records")[:1000]):
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

timeouts_df.to_csv(os.path.join("results", "AITK552_queries_answers1000.csv"), sep="\t", index=False)
