# Script Version 2.

import csv
import requests


URL = "http://0.0.0.0:8000/users"
PARAMETERS = {  "Nombre" : "name",
            "Ciudad" : "city",
            "Codigo Postal": "postalCode",
}
HEADERS = None
PATH_DATA = None
SPLIT_CHAR = "."
FILE_NAME = 'archivo.csv'
CHAR_DELIMITER = "\t"
METHOD = "get"
PAYLOAD = None
TIME_OUT = 10


title_keys_path = list(PARAMETERS.keys())
writer = csv.writer(open(FILE_NAME, "w" , encoding = "utf-8"), delimiter = CHAR_DELIMITER)
writer.writerow(title_keys_path)


def get_property(path,data):
    """Guarda temporalmente una llave y valida si hay mas diccionarios en el mismo"""
    path_keys = path.split(SPLIT_CHAR)
    element = data
    print(element)
    for key in path_keys:
        element = element.get(key)
    return element

def get_data_from_json(response):
    """Valida si necesita entrar mas de una vez a un json"""
    if PATH_DATA is None:
        return response.json()
    return get_property(PATH_DATA, response.json())

def write_data_to_csv(content):
    """Escribe en un doc csv datos"""
    for element in content:
        data = list()
        for key in title_keys_path:
            data.append(get_property(PARAMETERS.get(key), element))
        writer.writerow(data)

def send_request():
    """Determina si es necesario un get o post"""
    if METHOD == "get":
        return requests.get(URL, headers=HEADERS, timeout=TIME_OUT)
    return requests.post(URL, headers=HEADERS, timeout=TIME_OUT, data=PAYLOAD)


write_data_to_csv(
    get_data_from_json(
        send_request()
        )
)
