"""Команда создания базы данных Django (DjangoDB)"""
from django.core.management import BaseCommand
import pyodbc
from config.settings import DATABASE, USER, PASSWORD, HOST

class Command(BaseCommand):
    def handle(self, *args, **options):

        try:
            conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+HOST+';DATABASE='+DATABASE+';UID='+USER+';PWD='+PASSWORD)
            conn.autocommit = True
            conn.execute(fr"CREATE DATABASE DjangoDB")
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            print("Created DATABASE")
        finally:
            conn.close()