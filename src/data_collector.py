from typing import List, Optional

import requests


def get_company_data(company_id: str) -> Optional[dict]:
    """Получение данных о работодателе"""
    response = requests.get(f"https://api.hh.ru/employers/{company_id}")
    return response.json() if response.status_code == 200 else None


def get_vacancies_by_company(company_id: str) -> List[dict]:
    """Получение вакансий работодателя"""
    vacancies = []
    page = 0
    while True:
        response = requests.get(
            "https://api.hh.ru/vacancies",
            params={"employer_id": company_id, "page": page},
        )
        data = response.json()
        vacancies.extend(data["items"])
        if len(data["items"]) < 100 or (data["pages"]) <= page + 1:
            break
        page += 1
        return vacancies
