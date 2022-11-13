import mysql.connector
from dotenv import load_dotenv
import json
import os

class DatabaseManager():
                
    def __init__(self):
        # Load environment variables:
        load_dotenv()
        
        # Define:
        # - absolute path of this file in system
        # - name of file containing database structure
        # - charset and collation of database
        self.absolute_path          = os.path.dirname(os.path.abspath(__file__))
        self.tables_schema_filename = 'db_tables_schema.json'
        self.charset                = 'utf8mb4'
        self.collation              = 'utf8mb4_unicode_ci'

        # Stablish connection with database:
        self.conn = mysql.connector.connect(
            user     = os.getenv('DB_USER'),
            password = os.getenv('DB_PASS'),
            database = os.getenv('DB_NAME'),
            host     = os.getenv('DB_HOST')
        )
        
        self.db_cursor = self.conn.cursor()
        
        # Setup database if needed:
        self.init_database()
    
    
    def init_database(self):
        """
        Intilialize database.
        Create all tables needed for the telelgram bot to run.
        Only used for setup, if the tables are created, nothing happens.
        """
        
        # Load database schema:
        tables_schema = open('%s/%s' % (self.absolute_path, self.tables_schema_filename))
        tables = json.load(tables_schema)
        
        # Create all tables defined in the schema:
        [self.create_table(table) for table in tables]
            
    
    def create_table(self, table):
        """Executes the create table statement, given the table object.

        Args:
            table: dict
                A dictionary including de following fields:
                table_name: the name of the table it is going to be created
                fields: field
                    An array of fields that the table is going to have. Each field is a dict with
                        the following fields:
                        name(string!): --self-explanatory--
                        type(string!): --self-explanatory--
                        is_null(boolean!): --self-explanatory--
                        is_pk(boolean!): Whether the field is primary key or not
                        default(String): The default value of the field if none is specified
                        
        """
        create_table_sql  = 'CREATE TABLE IF NOT EXISTS %s (' % table['table_name']
        create_table_sql += ', '.join(map(self.define_field_sql, table['fields']))
        create_table_sql += ') DEFAULT CHARACTER SET %s COLLATE %s' % (self.charset, self.collation)
    
        self.db_cursor.execute(create_table_sql)
            
    def define_field_sql(self, field):
        """Create SQL string of a database table field

        Args:
            field: dict
                Info of the the field:
                name(string!): --self-explanatory--
                type(string!): --self-explanatory--
                is_null(boolean!): --self-explanatory--
                is_pk(boolean!): Whether the field is primary key or not
                default(String): The default value of the field if none is specified

        Returns:
            string: sql string for defining de table field
        """
        field_sql = '%s %s' % (field['name'], field['type'])
        
        # Check if field is not null
        field_sql += ' %sNULL' % ('NOT ' if not field['is_null'] else '')
        
        # Add default value:
        if not field['default'] is None: field_sql += ' DEFAULT %s' % field['default']
            
        # Check if field is primary key
        if field['is_pk']: field_sql += ' PRIMARY KEY'
        
        return field_sql


    def save(self, table, data):
        """Save data into the selected table

        Args:
            table: string
                Name of the database table
            data: dict
                Structure with the data required according to the table
        """
        
        insert_sql  = 'INSERT INTO %s SET ' % table
        insert_sql += ', '.join(map(lambda field: "{} = %s".format(field), data))

        self.db_cursor.execute(insert_sql, list(data.values()))
        self.conn.commit()
        
    def get_chat_by_id(self, chat_id ):
        self.db_cursor.execute("SELECT * FROM Chat WHERE id = %s", [chat_id])
        return self.db_cursor.fetchall()
    
    def get_chat_by_title(self, chat_title ):
        self.db_cursor.execute("SELECT * FROM Chat WHERE title = %s", [chat_title])
        return self.db_cursor.fetchall()