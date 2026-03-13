from typing import List, Optional, Tuple

import psycopg2


class DBManager:
    def __init__(
        self, db_name: str, user: str, password: str, host: str = "localhost"
    ) -> None:
        """Конструктор класса для управления базой данных PostgreSQL."""
        self.conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host
        )

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получение списка компаний и количества вакансий каждой из них."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT companies.name, COUNT(vacancies.id) AS vacancies_count
            FROM companies LEFT JOIN vacancies ON companies.id = vacancies.employer_id
            GROUP BY companies.id
        """)
        return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple]:
        """Получение всех вакансий с информацией о компаниях."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT companies.name, vacancies.title, vacancies.salary_from, vacancies.salary_to, vacancies.alternate_url
            FROM vacancies INNER JOIN companies ON vacancies.employer_id = companies.id
        """)
        return cursor.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Вычисление средней зарплаты среди вакансий."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT AVG(salary_from) FROM vacancies")
        result = cursor.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self) -> List[Tuple]:
        """Выборка вакансий с зарплатой выше среднего уровня."""
        avg_salary = self.get_avg_salary()
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM vacancies
            WHERE salary_from > %s
        """,
            (avg_salary,)
        )
        return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple]:
        """Поиск вакансий по заданному ключевому слову."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM vacancies
            WHERE LOWER(title) LIKE %s
        """,
            ("%" + keyword.lower() + "%",),
        )
        return cursor.fetchall()
