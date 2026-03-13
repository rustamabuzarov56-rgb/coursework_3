from typing import Any

import psycopg2


def create_database(
    db_name: str, user: str, password: str, host: str = "localhost"
) -> bool:
    """Создание базы данных"""
    try:
        connection = psycopg2.connect(user=user, password=password, host=host)
        connection.autocommit = True
        cursor = connection.cursor()

        sql_create_db = f"CREATE DATABASE {db_name};"
        cursor.execute(sql_create_db)

        print(f"База данных {db_name} успешно создана")
        return True
    except Exception as e:
        print(f"Произошла ошибка при создании базы данных {e}")
        return False
    finally:
        if connection:
            cursor.close()
            connection.close()


def create_tables(conn: psycopg2.extensions.connection) -> None:
    """Создание таблиц в базе данных"""
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXIST companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                area VARCHAR(255),
                logo_url VARCHAR(255));
                """)
    cur.execute("""
                    CREATE TABLE IF NOT EXIST vacancies  (
                    vacancy_id SERIAL PRIMARY KEY,
                    title VARCHAR(255),
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    employer_id TNT REFERENCES companies(company_id)
                    alternate_url VARCHAR(255));
                    """)
    conn.commit()


def insert_company(
    conn: psycopg2.extensions.connection, company_data: dict[str, Any]
) -> int:
    """Вставка данных о компании в базу"""
    cur = conn.cursor()
    cur.execute(
        """
                   INSERT INTO companies (name, description, area, logo_url)
                   VALUES (%s, %s, %s, %s)
                   RETURNING id""",
        (
            company_data["name"],
            company_data["description"],
            company_data["area"]["name"],
            company_data["logo_urls"]["original"],
        ),
    )
    return cur.fetchone()[0]


def insert_vacancy(
    conn: psycopg2.extensions.connection, vacancy_data: dict[str, Any], employer_id: int
) -> None:
    """Вставка данных о вакансии в базу"""
    cur = conn.cursor()
    cur.execute(
        """
                    INSERT INTO vacancies (title, salary_from, salary_to, currency, employer_id, alternate_url)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
        (
            vacancy_data["name"],
            vacancy_data["salary"]["from"],
            vacancy_data["salary"]["to"],
            vacancy_data["salary"]["currency"],
            employer_id,
            vacancy_data["alternate_url"],
        ),
    )
    conn.commit()
