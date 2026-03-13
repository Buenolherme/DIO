import pandas as pd
import requests
import json

API_URL = "https://sdw-2023-prd.up.railway.app"


def extract_users(csv_file):

    df = pd.read_csv(csv_file)

    users = []

    for user_id in df["UserID"]:
        try:
            response = requests.get(f"{API_URL}/users/{user_id}")

            if response.status_code == 200:
                users.append(response.json())

        except:
            pass

    if not users:
        print("API fora do ar. Usando dados simulados")

        users = [
            {"id":1,"name":"Peter","news":[]},
            {"id":2,"name":"Hyago","news":[]},
            {"id":3,"name":"Jorge","news":[]},
            {"id":4,"name":"Samira","news":[]},
            {"id":5,"name":"Lidia","news":[]}
        ]

    return users


def transform(users):

    for user in users:

        message = f"""
        Olá {user['name']}!
        Que tal começar a investir hoje?
        Pequenas decisões financeiras podem
        construir um grande futuro.
        """

        user["news"].append({
            "icon":"https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "description":message.strip()
        })

    return users



def load(users):

    updated = []

    for user in users:

        try:
            requests.put(f"{API_URL}/users/{user['id']}", json=user)
        except:
            pass

        updated.append(user)

    with open("resultado_etl.json","w",encoding="utf-8") as f:
        json.dump(updated,f,indent=4,ensure_ascii=False)

    print("ETL finalizado. Arquivo salvo.")



users = extract_users("SDW2023.csv")
users = transform(users)
load(users)