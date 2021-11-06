import psycopg2
from psycopg2 import Error

import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

try:
    connection = psycopg2.connect(user=os.environ.get('PSQL_USERNAME'),
                                    password=os.environ.get('PSQL_PASSWORD'),
                                    host=os.environ.get('PSQL_HOST'),
                                    port=os.environ.get('PSQL_PORT'),
                                    database=os.environ.get('PSQL_NAME'))
    cursor = connection.cursor()

    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    cursor.execute("CREATE TABLE biztickermentions (id SERIAL PRIMARY KEY, ticker varchar NOT NULL, coinGeckoId varchar NOT NULL, mentionId integer NOT NULL, threadId integer NOT NULL, unixTime integer NOT NULL, dateTime timestamp,  UNIQUE (mentionId, ticker));")

    # cursor.execute("INSERT INTO biztickermentions (mentionId, ticker, threadId, unixTime) VALUES (%s, %s, %s, %s)", (100, "abc'def", 100, 100))
    connection.commit()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")