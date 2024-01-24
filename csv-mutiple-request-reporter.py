#Script Version 2.

import csv
import requests


URL = "https://swapi.dev/api/{}/{}/"
URL_PARAMETERS = ["category", "id"]
PARAMETERS = { "Nombre" : "name",
            "Color de piel" : "skin_color",
            "Fecha de nacimiento" : "birth_year",
            "Altura" : "height"

}
REPLACE_CHAR_URL = "{}"
HEADERS = None
PATH_DATA = None
SPLIT_CHAR = "."
FILE_NAME = "results.csv"
DATA_FIILE_NAME = "data.csv"
CHAR_DELIMITER = ','
METHOD = "get"
PAYLOAD = None
TIME_OUT = 10
data_list = []


title_keys_path = list(PARAMETERS.keys())
writer = csv.writer(open(FILE_NAME, "w" , encoding = "utf-8"), delimiter = CHAR_DELIMITER)
writer.writerow(title_keys_path)
data_csv_dict = {}


def csv_reader_file():
    """Lee un archivo csv"""
    with open(DATA_FIILE_NAME, newline="" , encoding="utf-8") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=CHAR_DELIMITER)
        index = 0
        for row in file_reader:
            if index == 0:
                for element in row:
                    data_csv_dict[element]= len(data_csv_dict)
            else:
                new_url = URL.format(*row)
                response = requests.get(new_url, headers=HEADERS, timeout=TIME_OUT)
                if 200 <= response.status_code <= 299:
                    write_row_to_csv(response.json())
            index += 1


def csv_files_generator():
    """Crea un archivo csv en cada ocasión que obtiene un response"""
    csv_reader_file()

def get_property(path,data):
    """Guarda temporalmente una llave y valida si hay mas diccionarios en el mismo"""
    path_keys = path.split(SPLIT_CHAR)
    element = data
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
        write_row_to_csv(element)

def write_row_to_csv(element):
    data = list()
    for key in title_keys_path:
        data.append(get_property(PARAMETERS.get(key), element))
    writer.writerow(data)

def send_request():
    """Determina si es necesario un get o post"""
    if METHOD == "get":
        return requests.get(URL, headers=HEADERS, timeout=TIME_OUT)
    return requests.post(URL, headers=HEADERS, timeout=TIME_OUT, data=PAYLOAD)




csv_files_generator()