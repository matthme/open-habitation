import pandas as pd
import sqlalchemy
import dotenv
import os

'''
This file is meant to be run when the PostgreSQL instance for the API is instantiated.

.csv files which are to be loaded into the database are downloaded from URLs and
PostgreSQL tables are generated from them.
'''


dotenv.load_dotenv()

local_database = os.getenv("LOCAL_DATABASE")

if local_database=="true":
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    database = os.getenv("DATABASE")

    DATABASE_URL_SQLALCHEMY = "postgresql://" + username +":" + password + "@" + host + ":" + port + "/" + database


else: # taylored for heroku deployment:
    DATABASE_URL = os.environ['DATABASE_URL']

    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL_SQLALCHEMY = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    else:
        DATABASE_URL_SQLALCHEMY = DATABASE_URL



# engine = sqlalchemy.create_engine(DATABASE_URL_SQLALCHEMY, execution_options=dict(stream_results=True))
engine = sqlalchemy.create_engine(DATABASE_URL_SQLALCHEMY)



download_paths = {
    "electricityProduction_TABLE.csv": os.environ('ELECTRICITY_PRODUCTION_TABLE_URL'),
    "gwr_TABLE.csv": os.environ('GWR_TABLE_URL'),
    "heatingInfo_TABLE.csv": os.environ('HEATING_INFO_TABLE_URL')
}

filenames = {"electricityProduction_TABLE.csv":"electricity_production", "gwr_TABLE.csv":"gwr", "heatingInfo_TABLE.csv":"heating_info"}


for filename, table_name in filenames.items():

    print("Downloading '%s'..." %filename)
    chunks = pd.read_csv(download_paths[filename], index_col=0, chunksize=30000)
    print("Writing to table %s..." %table_name)
    counter = 0
    for df in chunks:
        try:
            df.to_sql(table_name, engine, if_exists="fail", chunksize=10000)
            print("Writing chunk %s" %counter)
            counter += 1

        except ValueError as e:
            if str(e) == "Table '%s' already exists." %table_name and counter==0:

                if local_database=="true":
                    # on own server/ local machine
                    while True:
                        answer = input("Table '%s' already exists. Do wou want to overwrite it (o) or skip it (s)?" %table_name)
                        if answer=="o" or answer=="O":
                            print("Writing chunk %s" %counter)
                            df.to_sql(table_name, engine, if_exists="replace")
                            counter += 1
                            break
                        elif answer=="s" or answer=="S":
                            break
                        else:
                            continue
                    pass

                else:
                    # always overwrite on heroku:
                    print("Overwriting existing table.")
                    print("Writing chunk %s" %counter)
                    df.to_sql(table_name, engine, if_exists="replace")
                    counter += 1

            elif str(e) == "Table '%s' already exists." %table_name and counter>0:
                # append:
                print("Writing chunk %s" %counter)
                df.to_sql(table_name, engine, if_exists="append")
                counter += 1

            else:
                raise e

print("Filling database complete.")