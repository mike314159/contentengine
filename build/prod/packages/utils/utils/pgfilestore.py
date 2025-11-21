



import os
import psycopg2
import time
import pandas as pd
import pytz

'''

write a python class that supports storing and retrieving large blobs of text or binary content in a postgres database. 
It should have methods for each of the following operations. 

use table name file_storage, in schema public, in db pc.
class name is PGFileStore

def save_file(id, src_local_filename):
    # id is a string and a unique key used to identify this file in other operations. 
    # function will read in the local file and store it in the DB
    # if a file with the same id already exists, it should be overwritten.
    # columns in the DB are
    #    id
    #    file_name
    #    file_content
    #    last_mod_ts, a unix timestamp of the last modified time of the local filename at the time it is stored in the DB.
    #    upload_ts, a unix timestamp of the time the file was uploaded to the DB.
    #    source_system, a string that identifies the system that uploaded the file.
    #    application, a string that identifies the name of the application this file relates to.
    
def pull_file(id, dest_local_filename, after_ts):
    # retrieve the file by the given id, and store it locally in dest_local_filename. 
    # the file written should have the last_mod_ts from the database. 
    # after_ts is optional. if the file in the DB has a last_mod_ts that is older than after_ts, return False and do not pull the file. 
    # return True if the file was successfully pulled and written to the local file, False otherwise.
    
def delete_file(id):
    # delete the file with the given id from the DB.

def file_exists(id):
    # return True if a file with the given id exists in the DB, False otherwise. 

Generate a python class that implements this class. 
Thoroughly comment the class and methods that make it easy to verify the class meets all of the specifications. 
Use print statments to output a log of the class's operations along with success or failure. 
Include as a comment at the top of the class all of the SQL needed to create the table in the database. 
Drop the table if the name already exists before creating it.
You should only generate the commented code, do not provide commentary or explanations.


Write unit tests (that will be stored in another file) that achieve a very high rate of test coverage for the class FileStorage. 
Dont use mocks, use the actual DB, but dont delete the table or modify its schema because it is being used by other applications. 
Put all test content under the application called 'pytest'.
I want you to use the pytest framework to write the tests.


'''


import os
import psycopg2
import time

class PGFileStore:
    """
    Class to store and retrieve large blobs of text or binary content in a PostgreSQL database.
    Uses a specific table in the 'public' schema on database 'pc' to manage files.

    SQL to set up the database table:
    CREATE TABLE IF NOT EXISTS public.file_storage (
        id TEXT PRIMARY KEY,
        file_name TEXT,
        file_content BYTEA,
        last_mod_ts BIGINT,
        upload_ts BIGINT,
        collection TEXT,
        application TEXT
    );
    """

    def __init__(self, app, collection, db_config):
        """
        Initializes the database connection using provided db_config and ensures the table exists.
        db_config should be a dictionary with keys: dbname, user, password, host
        """
        self.conn = psycopg2.connect(**db_config)
        self.ensure_table_exists()
        self.app = app
        self.collection = collection
        print("Database connection initialized and table checked/created.")

    def ensure_table_exists(self):
        """
        Ensures the 'file_storage' table exists in the database.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.file_storage (
                    id TEXT PRIMARY KEY,
                    file_name TEXT,
                    file_content BYTEA,
                    last_mod_ts BIGINT,
                    upload_ts BIGINT,
                    collection TEXT,
                    application TEXT
                );
            """)
            self.conn.commit()
            print("Table verified/created.")

    # For situations where multiple machines are writing to the db, we need to specify
    # a cross-machine last_update_ts. It shouldn't be based on the local machine's time
    # but rather something in the file itself.
    def save_file(self, id, src_local_filename, last_mod_ts):
        """
        Saves or updates a file in the database with given id and source file.
        """
        try:
            with open(src_local_filename, 'rb') as file:
                content = file.read()
                #last_mod_ts = int(os.path.getmtime(src_local_filename))
                upload_ts = int(time.time())
                file_name = os.path.basename(src_local_filename)

                with self.conn.cursor() as cur:
                    # Remove the existing file if it exists
                    sql = "DELETE FROM public.file_storage WHERE id = '%s' and application = '%s' and collection = '%s'" % (id, self.app, self.collection)
                    #print("Executing: ", sql)
                    cur.execute(sql)
                    
                    #sql = "INSERT INTO public.file_storage (id, application, collection, file_name, file_content, last_mod_ts, upload_ts) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    # Insert the new file entry
                    cur.execute("""
                        INSERT INTO public.file_storage (id, application, collection, file_name, file_content, last_mod_ts, upload_ts)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (id, self.app, self.collection, file_name, content, last_mod_ts, upload_ts))
                    
                    self.conn.commit()
                    print("PGFileStore: File %s saved successfully." % src_local_filename)
                    return True
        except Exception as e:
            print(f"Failed to save file: {e}")
            return False

    def pull_file(self, id, dest_local_filename, after_ts=None):
        """
        Retrieves a file from the database by id and saves it locally.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT file_content, last_mod_ts FROM public.file_storage WHERE id = %s and application = %s and collection = %s", (id,self.app,self.collection))
                result = cur.fetchone()
                if result:
                    file_content, last_mod_ts = result
                    if after_ts is not None and last_mod_ts < after_ts:
                        print("File timestamp is older than specified after_ts.")
                        return False
                    
                    with open(dest_local_filename, 'wb') as file:
                        file.write(file_content)
                        os.utime(dest_local_filename, (last_mod_ts, last_mod_ts))
                    
                    print("File pulled successfully.")
                    return True
        except Exception as e:
            print(f"Failed to pull file: {e}")
        return False

    def delete_file(self, id):
        """
        Deletes a file from the database by id.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM public.file_storage WHERE id = %s and application = %s and collection = %s", (id, self.app, self.collection))
                self.conn.commit()
                if cur.rowcount:
                    print("File deleted successfully.")
                    return True
                else:
                    print("No file found to delete.")
                    return False
        except Exception as e:
            print(f"Failed to delete file: {e}")
            return False

    def file_exists(self, id):
        """
        Checks if a file exists in the database by id.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT 1 FROM public.file_storage WHERE id = %s and application = %s and collection = %s", (id,self.app, self.collection))
                return cur.fetchone() is not None
        except Exception as e:
            print(f"Failed to check if file exists: {e}")
           
    def list_file_ids(self):
        """
        Lists all file IDs in the database for the specified application and collection.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM public.file_storage WHERE application = %s AND collection = %s", (self.app, self.collection))
                ids = cur.fetchall()
                return [id[0] for id in ids] if ids else []
        except Exception as e:
            print(f"Failed to list file IDs: {e}")
            return []


    def get_file_details(self, id):
        """
        Retrieves all details for a file in the database by its ID.
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT id, file_name, last_mod_ts, upload_ts, collection, application
                    FROM public.file_storage
                    WHERE id = %s AND application = %s AND collection = %s
                """, (id, self.app, self.collection))
                result = cur.fetchone()
                if result:
                    file_details = {
                        'id': result[0],
                        'file_name': result[1],
                        'last_mod_ts': result[2],
                        'upload_ts': result[3],
                        'collection': result[4],
                        'application': result[5]
                    }
                    return file_details
                else:
                    print("No file found with ID:", id)
                    return None
        except Exception as e:
            print(f"Failed to retrieve file details: {e}")
            return None


    # Sync a local cache with the remote store
    def sync(local_cache, pg_store, last_mod_func, download=True, upload=True, dry_run=False):

        local_ids = local_cache.list_ids()
        pg_ids = pg_store.list_file_ids()

        # Convert lists to sets for set operations
        local_id_set = set(local_ids)
        pg_id_set = set(pg_ids)

        local_only_ids = list(local_id_set - pg_id_set)  # IDs that are only in the local cache
        pg_only_ids = list(pg_id_set - local_id_set)     # IDs that are only in the PostgreSQL database
        common_ids = list(local_id_set & pg_id_set)      # IDs that are common to both

        print("Local Only IDs:", local_only_ids)
        print("PostgreSQL Only IDs:", pg_only_ids)
        print("Common IDs:", common_ids)

        download_ids = pg_only_ids
        upload_ids = local_only_ids

        print("Working on Common Ids")
        for id in common_ids:
            print("Checking ID ", id)
            #local_last_mod_ts = last_mod_func(local_cache, id)
            local_last_mod_ts = local_cache.get_last_modified_ts(id)

            details = pg_store.get_file_details(id)
            #print(json.dumps(details, indent=4))
            remote_last_mod_ts = details.get('last_mod_ts', 0)

            if local_last_mod_ts < remote_last_mod_ts:
                print("Local file is older than PG, add to download list.")
                download_ids.append(id)
            else:
                if local_last_mod_ts > remote_last_mod_ts:
                    print("Local file (%d) is newer than PG (%d). Add to upload list." % (local_last_mod_ts, remote_last_mod_ts))
                    upload_ids.append(id)
                else:
                    print("Local file has same timestamp as PG, do nothing")
                    pass

        if download:
            print("\nDownload IDs: ", download_ids)
            if dry_run:
                print("Dry run, do NOT download files.")
            else:
                for id in download_ids:
                    local_fn = local_cache._get_fn(id)
                    print("Pulling ID ", id, ' saving to ', local_fn)
                    pg_store.pull_file(id, local_fn)

        if upload:
            print("\nUpload IDs: ", upload_ids)
            if dry_run:
                print("Dry run, do NOT upload files.")
            else:
                for id in upload_ids:
                    local_fn = local_cache._get_fn(id)
                    print("Uploading ID ", id)
                    local_last_mod_ts = last_mod_func(local_cache, id)
                    pg_store.save_file(id, local_fn, local_last_mod_ts)


    def add_localized_date_column(self, df, col_name):
        """
        Adds a formatted date column to a dataframe.
        """
        tmp_col_name = f'tmp_{col_name}'
        df[tmp_col_name] = pd.to_datetime(df[col_name], unit='s', utc=True)

        # add a column for current utc time
        #df['current_utc_dt'] = pd.to_datetime('now', utc=True)
        #df['ago'] = df['current_utc_dt'] - df['tmp_added_ts']
        #df['ago'] = df['ago'].dt.floor('s')

        new_col_name = f'{col_name}_pt_dt'
        california_tz = pytz.timezone('America/Los_Angeles')
        df[new_col_name] = df[tmp_col_name].dt.tz_convert(california_tz)
        df.drop(columns=[tmp_col_name], inplace=True)


    def get_file_df(self): # , application=None, collection=None):
        """
        Queries the database and returns a dataframe with all columns in the file_storage table except file_content.
        Allows filtering by application and collection.
        """
        try:
            query = "SELECT id, file_name, last_mod_ts, upload_ts, collection, application FROM public.file_storage WHERE 1=1"
            params = []
            # if application:
            #     query += " AND application = %s"
            #     params.append(application)
            # if collection:
            #     query += " AND collection = %s"
            #     params.append(collection)
            
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                df = pd.DataFrame(rows, columns=['id', 'file_name', 'last_mod_ts', 'upload_ts', 'collection', 'application'])

                if df is not None and len(df) > 0:
                    self.add_localized_date_column(df, 'last_mod_ts')
                    self.add_localized_date_column(df, 'upload_ts')
                    df.sort_values(by='last_mod_ts', ascending=False, inplace=True)

                return df
        except Exception as e:
            print(f"Failed to retrieve file dataframe: {e}")
            return None