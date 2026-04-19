#!/usr/bin/python3
from PyQt5.QtSql import QSqlQuery


#def create_tables(query):
def create_tables(db):#
    query = QSqlQuery(db)#
    sequences = [
        """CREATE SEQUENCE public.kluch_slova_id_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",

        """CREATE SEQUENCE public.kluch_slova_ssylka_id_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",

        """CREATE SEQUENCE public.polzovateli_id_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",

        """CREATE SEQUENCE public."razdel/ssylka_id_seq"
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",

        """CREATE SEQUENCE public.razdely_id_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",

        """CREATE SEQUENCE public.ssylki_tab_id_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",

        """CREATE SEQUENCE public.zakladki_id_seq
            AS integer
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1""",
    ]

    tables = [
        """CREATE TABLE public.cluch_slova (
            id integer NOT NULL,
            slovo text
        )""",

        """CREATE TABLE public.cluch_slova_ssylka (
            id integer NOT NULL,
            id_ssylka integer,
            id_cluch_slova integer
        )""",

        """CREATE TABLE public.polzovateli (
            id integer NOT NULL,
            login text,
            parol text,
            yr_dopuska text
        )""",

        """CREATE TABLE public.razdel_ssylka (
            id integer NOT NULL,
            id_razdela integer,
            id_ssylki integer
        )""",

        """CREATE TABLE public.razdely (
            id integer NOT NULL,
            razdel text
        )""",

        """CREATE TABLE public.ssylki_tab (
            id integer NOT NULL,
            naimen text,
            ssylka text,
            opisanie text,
            skrinshot bytea
        )""",

        """CREATE TABLE public.zakladki (
            id integer NOT NULL,
            id_ssylka integer,
            id_polz integer
        )""",
    ]

    defaults = [
        """ALTER TABLE ONLY public.cluch_slova ALTER COLUMN id SET DEFAULT nextval('public.kluch_slova_id_seq'::regclass)""",

        """ALTER TABLE ONLY public.cluch_slova_ssylka ALTER COLUMN id SET DEFAULT nextval('public.kluch_slova_ssylka_id_seq'::regclass)""",

        """ALTER TABLE ONLY public.polzovateli ALTER COLUMN id SET DEFAULT nextval('public.polzovateli_id_seq'::regclass)""",

        """ALTER TABLE ONLY public.razdel_ssylka ALTER COLUMN id SET DEFAULT nextval('public."razdel/ssylka_id_seq"'::regclass)""",

        """ALTER TABLE ONLY public.razdely ALTER COLUMN id SET DEFAULT nextval('public.razdely_id_seq'::regclass)""",

        """ALTER TABLE ONLY public.ssylki_tab ALTER COLUMN id SET DEFAULT nextval('public.ssylki_tab_id_seq'::regclass)""",

        """ALTER TABLE ONLY public.zakladki ALTER COLUMN id SET DEFAULT nextval('public.zakladki_id_seq'::regclass)""",
    ]

    for sql in sequences:
        #query.exec_(sql)
        try: query.exec_(sql)#
        except: pass # Игнорируем ошибки, если секвенция уже есть

    for sql in tables:
        query.exec_(sql)

    for sql in defaults:
        query.exec_(sql)


def check_and_create_database(db):
    #
    # if not db.isOpen():
    #     print("База данных не открыта.")
    #     return False
    #

    query = QSqlQuery()

    query.exec_("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ssylki_tab')")
    
    tables_exist = False
    if query.next():
        tables_exist = query.value(0)

    if tables_exist:
        print('Таблицы уже существуют.')
        return True

    print('Таблицы не найдены. Создаем таблицы...')
    create_tables(query)

    query.exec_("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ssylki_tab')")
    if query.next() and query.value(0):
        print('Таблицы успешно созданы.')
        return True
    else:
        print('Ошибка при создании таблиц.')
        return False

