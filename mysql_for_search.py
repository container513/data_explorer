from full_text_search import FullTextSearch
from nltk_analyzer import NltkAnalyzer
import mysql.connector
import json

class MysqlForSearch(FullTextSearch):
    def __init__(self, uri, user, password, database):
        self.driver = mysql.connector.connect(host=uri, user=user, password=password, database=database)
        self.data = []
        self.database = database
        self.analyzer = NltkAnalyzer()



    def search_keyword(self, keyword):
        db_cursor = self.driver.cursor()

        # To find all the tables in database
        db_cursor.execute('use {}'.format(self.database))
        db_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '{}'".format(self.database))
        all_tables_result = [tables[0] for tables in db_cursor.fetchall()]
        all_tables_result.remove('user')

        # To find all the columns in each table
        table_map_columns_dict = dict()
        data_type = ('varchar', 'text', 'char')
        params = ', '.join(['%s']*len(data_type))

        query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %s and table_schema = %s and DATA_TYPE in ({c})".format(c=params)

        for table in all_tables_result:
            db_cursor.execute(query, (table, self.database, *data_type))
            results = db_cursor.fetchall()
            columns_table = [r[0] for r in results]
            table_map_columns_dict[table] = columns_table

        # To export the data from each table
        table = ''
        query = ""

        table_map_json = dict()

        for key, value in table_map_columns_dict.items():
            if len(value) == 0:
                continue
            
            query = "select JSON_ARRAYAGG(JSON_OBJECT({0})) from {1}".format(', '.join(f'"{v}", {v}' for v in value), key)
            
            db_cursor.execute(query)
            results = db_cursor.fetchall()
            table_map_json[key] = [json.loads(d[0]) for d in results][0]


        # Find all the tables and columns that match key in the dictionary.
        search_results = []
        search_results_table_column = []
        table_total = []
        for key_table, value_table in table_map_json.items():
            if len(value) == 0:
                continue

            total = 0
            # table name match 
            if keyword in key:
                total = total+1
                search_results.append({'table_name': key_table, 'column_name': '', 'columns_value': key_table, 'frequency': key_table.count(keyword)})

            # column name match
            for key_column, value_column in value_table[0].items():
                if keyword in key_column:
                    total = total+1
                    search_results.append({'table_name': key_table, 'column_name': key_column, 'columns_value': key_column, 'frequency': key_column.count(keyword)})

            # column value match
            for v in value_table:
                for key_column, value_column in v.items():
                    total_column = 0
                    if value_column is None:
                        continue
                    if keyword in value_column:
                        total = total + 1
                        search_results.append({'table_name': key_table, 'column_name': key_column, 'columns_value': value_column, 'frequency': value_column.count(keyword)})
                    
                    self.analyzer.analyze(key_table, key_column, value_column, keyword)

            table_total.append({"table_name": key_table, "frequency": total});  
        
        db_cursor.close()
        return self.analyzer.bigram_counts