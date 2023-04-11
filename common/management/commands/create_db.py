from django.core.management.base import BaseCommand
from django.conf import settings
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Command(BaseCommand):
    help = 'Creates the database specified in settings.py'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        dbname = db_settings['NAME']
        user = db_settings['USER']
        password = db_settings['PASSWORD']
        host = db_settings['HOST']
        port = db_settings['PORT']

        con = None
        try:
            con = connect(
                dbname='postgres',
                user=user,
                password=password,
                host=host,
                port=port
            )

            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            cur.execute(f'CREATE DATABASE {dbname};')
            self.stdout.write(self.style.SUCCESS(f'Database "{dbname}" created successfully'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        finally:
            if con:
                con.close()
