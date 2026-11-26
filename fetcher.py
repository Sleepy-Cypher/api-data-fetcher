import csv
import requests
import json 


def load_config(path):
    try: 
        with open(path+"/"+"config.json", "r", encoding="utf-8") as file:
            json_conv=json.load(file)
            return json_conv
    except FileNotFoundError:
        print("File not found.")
        return None
def fetch_data(url, params, headers):
    try:
        response= requests.get(url, params=params, headers=headers, timeout=10) 
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        print("HTTPError")
    except requests.exceptions.RequestException as e:
        print("Bad connection", e)
    return None
def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
         json.dump(data, file, indent=2)
def save_csv(rows, filename):
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer=csv.DictWriter(file, fieldnames=["topic", "page"])
        writer.writeheader()
        writer.writerows(rows)
def main():
    url= "https://httpbin.org/get"
    params={"topic": "fake-news", "page": 3}
    headers={}
    key= load_config(".")
    headers["X-Fake-Key"]= key["api_key"]
    data= fetch_data(url, params, headers)
    if None in [data, key]:
        print("something went wrong")
        return 
    save_json(data["args"], "result.json")
    save_csv([data["args"]], "result.csv")
    print("Saved")

if __name__=="__main__":
    main()

