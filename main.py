import os
from src.utils import get_vacancies, get_employer, create_database, save_data_to_database
from src.config import config
from pprint import pprint
import requests

def main():
    # Получаем данные о компаниях и их вакансиях по API, создаем базу данных и таблицы, и заполняем их.
    employer_list = [1740, 87021, 2180, 4180, 80, 2343, 78638, 3529, 4023, 543636]

 #    employer_list = [{'employer': [1740, 'Яндекс']},
 # {'employer': [2180, 'Ozon']},
 # {'employer': [67611, 'Тензор']}]
 # # {'employer': [3529, 'СБЕР', 6593]},
 # # {'employer': [4181, 'Банк ВТБ (ПАО)', 2452]},
 # # {'employer': [6591, 'ПСБ (ПАО «Промсвязьбанк»)', 1154]},
 # # {'employer': [1455, 'HeadHunter', 66]},
 # # {'employer': [15478, 'VK', 478]},
 # # {'employer': [64174, '2ГИС', 380]},
 # # {'employer': [3713346, 'Славнефть-ЯНОС', 13]}]
    params = config()
    # p = get_vacancies(employer_list)
    # pprint(p)
    s = get_employer(employer_list)
    pprint(s)


    # create_database('hh', params)
    # save_data_to_database(, 'hh', params)


if __name__ == '__main__':
    main()