Проект реализован для получения данных о вакансиях с сайта HeadHunter и последующим сохранением их в базу данных. Используемая СУБД - PostgreSQL.

База данных имеет две таблицы: employers и employers_vacancy. 

В таблице employers хранятся:
id компании,
название компании

В таблице employers_vacancy хранятся:
id вакансии,
id компании,
название вакансии,
заработная плата,
ссылка на вакансию

Чтобы начать работать с программой, необходимо указать название БД для сохранения в нее информации.

Пользователь имеет возможность выбрать следующие критерии отбора вакансий:
получить список всех компаний и количество вакансий у каждой компании
получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
получить среднюю зарплату по вакансиям
получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
получить список всех вакансий, в названии которых содержатся переданные в метод слова
