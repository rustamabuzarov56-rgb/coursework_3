import psycopg2
import configparser
from src.database_manager import create_tables, insert_company, insert_vacancy
from src.dbmanager import DBManager
from src.data_collector import get_company_data, get_vacancies_by_company

config = configparser.ConfigParser()
config.read('database.ini')

DB_NAME = config['postgresql']['dbname']
USERNAME = config['postgresql']['user']
PASSWORD = config['postgresql']['password']
HOST = config['postgresql']['host']
PORT = config['postgresql'].get('port', fallback=None)

def load_data_into_database():
    """Загрузка данных в базу данных."""
    conn = psycopg2.connect(dbname=DB_NAME, user=USERNAME, password=PASSWORD, host=HOST)
    create_tables(conn)
    create_tables(conn)

    company_ids = ['1', '2', '3']
    for cid in company_ids:
        company_data = get_company_data(cid)
        if company_data is not None:
            company_id = insert_company(conn, company_data)
            vacancies = get_vacancies_by_company(cid)
            for vacancy in vacancies:
                insert_vacancy(conn, vacancy, company_id)


def run_interface():
    """Простое меню для работы с программой."""
    manager = DBManager(DB_NAME, USERNAME, PASSWORD)
    while True:
        print("\nМеню:")
        print("1. Компании и количество вакансий.")
        print("2. Все вакансии.")
        print("3. Средняя зарплата.")
        print("4. Вакансии с зарплатой выше средней.")
        print("5. Вакансии по ключевому слову.")
        print("6. Выход.")
        choice = input("Ваш выбор: ")

        if choice == '1':
            results = manager.get_companies_and_vacancies_count()
            for row in results:
                print(row)
        elif choice == '2':
            results = manager.get_all_vacancies()
            for row in results:
                print(row)
        elif choice == '3':
            avg_salary = manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")
        elif choice == '4':
            results = manager.get_vacancies_with_higher_salary()
            for row in results:
                print(row)
        elif choice == '5':
            keyword = input("Введите слово для поиска: ")
            results = manager.get_vacancies_with_keyword(keyword)
            for row in results:
                print(row)
        elif choice == '6':
            break
        else:
            print("Некорректный ввод!")


if __name__ == '__main__':
    load_data_into_database()
    run_interface()