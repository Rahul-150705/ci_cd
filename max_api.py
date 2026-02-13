import pprint
from math import prod

import pandas as pd
import requests


session = requests.Session()

base_url = "https://www.maxfashion.in/in/en/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.maxfashion.in/",
    "Origin": "https://www.maxfashion.in"
}
home = session.get(base_url, headers=headers, timeout=5)

if home.status_code == 200:
    print("Homepage Loaded Successfully")
else:
    print("Failed To Load Homepage")
    print(home.status_code)
    exit()

output = []

page = 1
rows = 48
url = "https://search.unbxd.io/d11649dadd583dbf85dbd5eb928160e7/ss-unbxd-aapac-prod-Max-LandMark48741709218622/category"

offset = (page - 1) * rows
params = {
    "rows": "48",
    "page": "3",
    "pagetype": "boolean",
    "p": "allCategories_uFilter:maxmen-tops-polos",
    "facet": "true",
    "selectedfacet": "true",
    "facet.multiselect": "true",
    "fields": ",".join([
        "concept",
        "createDate",
        "employeePrice",
        "isConceptDelivery",
        "name",
        "percentageDiscount",
        "productType",
        "productCode",
        "color",
        "sibiling",
        "price",
        "productUrl",
        "childDetail",
        "summary",
        "uniqueId",
        "wasPrice",
        "imageUrl",
        "gallaryImages",
        "badgeVisible",
        "inStock",
        "approvalStatus",
        "stats",
        "sislogo"
    ]),
    "filter": [
        'inStock:"1"',
        'approvalStatus:"1"'
    ],
    "stats": "price"
}
response = session.get(url, params=params, headers=headers, timeout=20)
if response.status_code != 200:
    print("Page Failed")
data = response.json()
prod = data["response"]["products"]
for product in prod:
    price_info = product.get("price", {})
    product_name=product.get("name")
    product_url=product.get("productUrl")
    mrp=product.get("wasPrice")
    id=product.get("uniqueId")
    output.append([id,product_name, price_info,mrp, product_url])
df = pd.DataFrame(output)

df.to_json("tata_json.json", orient="records", indent=4)
df.to_csv("tata_csv.csv", index=False)

print(f"Saved {len(output)} products.")

