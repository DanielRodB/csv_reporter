#Script Version 2.

import csv
import json
import requests

URL = "http://0.0.0.0:8000/users/batch"
URL_PARAMETERS = ["id"]
PAYLOOAD_PARAMETERS = {
    "Id":{"name":"id",
        "position": 0},
    "Nombre":{"name":"firstName",
        "position": 1},
    "Apellido": {"name":"lastName",
        "position": 2},
}

PARAMETERS = {
    "id": "id",
    "Nombre": "first_name",
    "Apellido": "last_name",
    "Numero de tel": "phone_numbers"
}
HEADERS = None
SPLIT_CHAR = "."
FILE_NAME = "results.csv"
DATA_FIILE_NAME = "data.csv"
CSV_FILE_TO_PAYLOAD = "data_payload.csv"
FILE_JSON = "payload.json"
CHAR_DELIMITER = ','
METHOD = "Post"
TIME_OUT = 10
ORIGINAL_PAYLOAD = ""
CHAR_DELIMITER_WRITER = "\t"

with open(FILE_JSON, 'r', encoding="utf-8") as file:
    ORIGINAL_PAYLOAD = file.read().rstrip()

title_keys_payload_path = list(PAYLOOAD_PARAMETERS.keys())
title_keys_path = list(PARAMETERS.keys())
writer = csv.writer(open(FILE_NAME, "w" , encoding = "utf-8"), delimiter = CHAR_DELIMITER_WRITER)
writer.writerow(title_keys_path)
data_csv_dict = {}


def csv_reader_file():
    """Lee un archivo csv"""
    if METHOD == "get":
        with open(DATA_FIILE_NAME, newline="" , encoding="utf-8") as csv_file:
            file_reader = csv.reader(csv_file, delimiter=CHAR_DELIMITER)
            index = 0
            for row in file_reader:
                if index != 0:
                    new_url = URL.format(*row)
                    response = send_request(new_url)
                    if 200 <= response.status_code <= 299:
                        write_row_to_csv(response.json())
                index += 1
    else:
        with open(CSV_FILE_TO_PAYLOAD, newline="", encoding="utf-8") as payload_file:
            file_data_payload = csv.reader(payload_file, delimiter=CHAR_DELIMITER)
            index = 0
            for row in file_data_payload:
                if index != 0:
                    json_payload = ORIGINAL_PAYLOAD
                    for key in title_keys_payload_path:
                        dict_payload = PAYLOOAD_PARAMETERS.get(key)
                        json_payload=json_payload.replace(
                            "{"+dict_payload.get("name")+"}",
                            row[dict_payload.get("position")]
                        )
                    response = send_request(URL,json.loads(json_payload))
                    print(response.json())
                    if 200 <= response.status_code <= 299:
                        write_row_to_csv(response.json())

                index += 1

def get_property(path,data):
    """Guarda temporalmente una llave y valida si hay mas diccionarios en el mismo"""
    path_keys = path.split(SPLIT_CHAR)
    element = data
    for key in path_keys:
        element = element.get(key)
    return element

def write_row_to_csv(element):
    """Escribe datos en el archivo csv"""
    data = list()
    for key in title_keys_path:
        data.append(get_property(PARAMETERS.get(key), element))
    writer.writerow(data)

def send_request(url, payload=None):
    """Determina si es necesario un get o post"""
    if METHOD == "get":
        return requests.get(url, headers=HEADERS, timeout=TIME_OUT)
    return requests.post(url, headers=HEADERS, timeout=TIME_OUT, json=payload)




csv_reader_file()
