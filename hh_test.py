# Python 3.XX

import requests
import json
from test_data import *
from threading import Thread

def test_areas():
    """
    Function tests get method of https://api.hh.ru/areas.
    """

    print("Started test_areas")

    res = requests.get(areas_url)

    try:
        assert res.status_code in codes_success, "Not success status code"  # 1.1

        json_list = json.loads(res.text)
        area_ids = []

        # takes id's of areas from json and put in the list
        def extract_ids(json_data):
            def parse_areas(areas):
                for area in areas.get("areas"):
                    if area["name"] == region_name:
                        global region_id
                        region_id = area.get("id")

                    area_ids.append(area.get("id"))
                    parse_areas(area)

            for top_level_area in json_data:
                if top_level_area["name"] == country_name:
                    global country_id
                    country_id = top_level_area.get("id")

                area_ids.append(top_level_area.get("id"))
                parse_areas(top_level_area)

        extract_ids(json_list)

        # positive - check id for existence

        def run_in_thread(fn):
            def run(*k, **kw):
                t = Thread(target=fn, args=k, kwargs=kw)
                t.start()
                return t

            return run

        @run_in_thread
        def check_areas_response(area_ids, thread_id):
            for id_area in area_ids:
                url = area_url.format(id_area)
                res = requests.get(url)
                # print("Requested", url, res.status_code, "in thread", thread_id)
                try:
                    assert res.status_code in codes_success, \
                        "Not success status code {} {}".format(url, res.status_code)  # 1.2
                except AssertionError as error:
                    print(error)

        threads = []
        for el in range(thread_count):
            thread_area_ids = [x for x in area_ids if area_ids.index(x) % thread_count is el]
            threads.append(check_areas_response(thread_area_ids, el + 1))

        for thread in threads:
            thread.join()

        print("Finished test_areas")

        # negative - check errors

        for el in invalid_area_ids:
            url = area_url.format(el)
            res = requests.get(url)

            assert res.status_code in codes_client_error, \
                "Not invalid status code {} {}".format(url, res.status_code)  # 1.3

    except AssertionError as error:
        print(error)


def test_employers():
    """
    Function tests get method of https://api.hh.ru/employers.
    """

    print("Started test_employers in country", country_name, country_id)

    payload_employers = dict()
    payload_employers["area"] = country_id
    payload_employers["text"] = company_name

    res = requests.get(employers_url, params=payload_employers)

    try:
        assert res.status_code in codes_success, "Not success status code"   # 2.1

        res_json = json.loads(res.text)

        assert res_json['found'] > 0, "Company not found"  # 2.2
        assert res_json['found'] == 1, "Found several companies with the same name"  # 2.3
        assert len(res_json['items']) == res_json['found'], "Items size and found count not equal"  # 2.4
        assert res_json['items'][0]["name"] == company_name, "Found different company"  # 2.5

        global company_id
        company_id = res_json['items'][0]["id"]
    except AssertionError as error:
        print(error)

    print("End test_employers")


def test_vacancy():
    """
    Function tests get method of https://api.hh.ru/vacancies.
    """

    print("Started test_vacancy for company", company_name, company_id)

    payload_vacancies = dict()
    payload_vacancies["area"] = region_id
    payload_vacancies["employer_id"] = company_id
    payload_vacancies["text"] = vacancy_name
    res = requests.get(vacancies_url, params=payload_vacancies)

    try:
        assert res.status_code in codes_success, "Not success status code"  # 3.1

        res_json = json.loads(res.text)
        assert res_json['found'] > 0, "Vacancy not found"  # 3.2
        assert len(res_json['items']) == res_json['found'], "Items size and found count not equal"  # 3.3

        for vacancy_json in res_json["items"]:
            assert vacancy_name.lower() in vacancy_json["name"].lower(), "Vacancy name is not corrent"  # 3.4

    except AssertionError as error:
        print(error)

    print("End test_vacancy")

