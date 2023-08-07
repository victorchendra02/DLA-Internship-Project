import psycopg2


class PostgreSQL:
    def __init__(self, 
                 database=None,
                 user='postgres',
                 password='admin',
                 host='localhost',
                 port= '5432'):

        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.__error_no_db_selected = "PostgreSQL not yet select to any db!"
        self.__error_no_such_db = "No such db in PostgreSQL!"
        self.__error_db_already_selected = "Db already selected to"
        self.__notify_switch_db = "Db switched"
    
    def __conn(self):
        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
            )
        conn.autocommit = True
        
        return conn
    
    def __cursor(self):
        cursor = self.__conn().cursor()
        return cursor
    
    def __close(self):
        return self.__conn().close()
    
    def select_db(self, dbname):
        if self.database == dbname:
            print(f"{self.__error_db_already_selected} '{self.database}'")
            return
        
        connection = psycopg2.connect(
            database='postgres', 
            user=self.user, 
            password=self.password, 
            host=self.host, 
            port=self.port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        
        # Check if the database already exists
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        if exists:
            if self.database is not None:
                print(f"{self.__notify_switch_db} from {self.database} to {dbname}")
            else:
                print(f"PostgreSQL selecting '{dbname}' db!")
            self.database = dbname
        else:
            print(f"{self.__error_no_such_db} '{dbname}'")
    
    def create_new_db(self, dbname):
        cursor = self.__cursor()
        cursor.execute(f"CREATE database {dbname};")
        self.__close()
        print("Database has been created successfully !!")

    def create_new_table(self, schema: str):
        # SCHEMA EXAMPLE:

        """
        CREATE TABLE
            employee(
                first_name CHAR(20) NOT NULL,
                last_name CHAR(20),
                age INT,
                sex CHAR(1),
                income FLOAT
            )
        """
        
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return
        
        cursor = self.__cursor()
        cursor.execute(schema)
        self.__close()
        print("Table has been created successfully !!")

    def drop_db(self, dbname):
        cursor = self.__cursor()
        cursor.execute(f"DROP database {dbname};")
        self.__close()
        print("Database dropped !!")

    def drop_table(self, table_name):
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return
        
        cursor = self.__cursor()
        cursor.execute(f"DROP table {table_name};")
        self.__close()
        print("Table dropped !!")

    def delete_record_table(self, table_name):
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return

        cursor = self.__cursor()
        cursor.execute(f"DELETE table {table_name};")
        self.__close()
        print("Record deleted !!")

    def get_column_name(self, table_name):
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return
        
        cursor = self.__cursor()
        cursor.execute(f"Select * FROM {table_name} LIMIT 0")
        colnames = [desc[0] for desc in cursor.description]
        self.__close()
        return colnames

    def insert_dataframe_into_db(self, table_name, df):
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return

        cursor = self.__cursor()
        colname = ", ".join(self.get_column_name(table_name))
        
        for i in range(df.shape[0]):
            temp = df.values[i]
            joined_str = ", ".join(f"'{value}'" if isinstance(value, str) else str(value) for value in temp)
            query = f"""\
            INSERT INTO {table_name}({colname})\n    VALUES({joined_str})
            """
            cursor.execute(query)
            print(f"({i+1}) {query.strip()}\n")
        
        self.__close()
        print("Successfully insert dataframe !!")
        
    def load_table(self, table_name):
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return
    
        cursor = self.__cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        results = cursor.fetchall()
        self.__close()

        return results
    
    def load_all_tables(self):
        if self.database is None:
            print(f"{self.__error_no_db_selected}")
            return
        
        cursor = self.__cursor()
        cursor.execute(
            """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """
        )
        list_all_table_names = cursor.fetchall()  # output: [('result1',), ('result2',)]
        result = []
        for table_name in list_all_table_names:
            result.append((table_name[0], self.load_table(table_name[0])))
        self.__close()
        
        return result
