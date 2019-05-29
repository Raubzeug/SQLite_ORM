import sqlite3

class Model:

    """to create new table we must create new class inherited from Model with class attributes
    that are columns of the future table.
    to create a new row in table we need to create an instance of the class"""
    def __init__(self, connection, **kwargs):
        self._con = connection
        columns = self.__class__.__dict__['columns']
        for col in columns:
            if col[1].pk or col[1].req:
                if col[0] not in kwargs:
                    raise AttributeError(f'{col[0]} must be given')
                else:
                    self.__dict__[col[0]] = kwargs[col[0]]
            else:
                if col[0] in kwargs:
                    self.__dict__[col[0]] = kwargs[col[0]]
                else:
                    self.__dict__[col[0]] = 'NULL'
        self._insert_data()

    def _insert_data(self):
        arg_names = [key for key in self.__dict__ if not key.startswith('_')]
        arg_values = [self.__dict__[key] for key in arg_names]

        for i in range(len(arg_values)):
            if isinstance(arg_values[i], int):
                arg_values[i] = str(arg_values[i])
            elif arg_values[i] != 'NULL':
                arg_values[i] = f'"{arg_values[i]}"'

        sql = f'INSERT INTO {self.__class__.__name__} ({", ".join(arg_names)}) VALUES ({", ".join(arg_values)});'
        cur = self._con.cursor()
        try:
            cur.execute(sql)
            print('Data successfully inserted')
        except sqlite3.Error as err:
            print('Insert failed', err)


    @classmethod
    def create_table(cls, con):
        columns = [(key, cls.__dict__[key]) for key in cls.__dict__.keys()
                   if not key.startswith('_')]
        setattr(cls, 'columns', columns)
        for col in columns:
            col[1].__dict__['name'] = col[0]

        table_name = cls.__name__.lower()
        sql = f'CREATE TABLE {table_name} ('
        fk = None
        for i in range(len(columns)):
            columns[i][1].__dict__['name'] = columns[i][0]
            columns[i][1].__dict__['table'] = cls.__name__
            if 'foreignkey' in columns[i][1].__dict__:
                fk = (columns[i][0], columns[i][1].__dict__['foreignkey'])
                setattr(cls, 'fk', fk)
                # print(cls.__name__, cls.__dict__)
            if i == len(columns) - 1:
                if fk == None:
                    sql += columns[i][0] + ' ' + str(columns[i][1]) + ');'
                else:
                    con.execute("PRAGMA foreign_keys = 1")
                    sql += columns[i][0] + ' ' + str(columns[i][1]) + ','
                    sql += f' FOREIGN KEY ({fk[0]}) REFERENCES {fk[1].table}({fk[1].name}));'
            else:
                sql += columns[i][0] + ' ' + str(columns[i][1]) + ',' + ' '
        cur = con.cursor()
        try:
            cur.execute(sql)
            print(f'table {table_name} successfully created')
        except sqlite3.Error as err:
            print('Table creation failed', err)

    @classmethod
    def drop_table(cls, con):
        table_name = cls.__name__.lower()
        sql = f'DROP TABLE {table_name}'
        cur = con.cursor()
        try:
            cur.execute(sql)
            print(f'table {table_name} successfully deleted')
        except sqlite3.Error as err:
            print('Delete operation failed', err)

    """to use the method you must transfer to it connection, columns as a list (example: columns = ['id', 'name'])
     and condition as a string (example: condition='id=3 and name="Joe"')"""
    @classmethod
    def select(cls, con, columns=None, condition=None):
        sql = 'SELECT '
        table_name = cls.__name__.lower()
        if columns:
            for col in columns:
                if col not in cls.__dict__:
                    raise AttributeError(f'"{col}" column not in table')
            sql += ', '.join(columns) + ' FROM '
        else:
            sql += '* FROM '

        sql += table_name

        if not condition:
            sql += ';'
        else:
            sql += f' WHERE {condition};'
        cur = con.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except sqlite3.Error as err:
            print(err)

    @classmethod
    def select_all(cls, con):
        return cls.select(con)

    @classmethod
    def delete(cls, con, condition=None):
        table_name = cls.__name__.lower()
        sql = f'DELETE FROM {table_name}'
        if not condition:
            sql += ';'
        else:
            sql += f' WHERE {condition};'
        cur = con.cursor()
        try:
            cur.execute(sql)
            print('data sucessfully deleted')
        except sqlite3.Error as err:
            print(err)

    def delete_instance(self):
        self.delete(self._con, condition=f'id={self.id}')

    @classmethod
    def update(cls, con, new_vals, condition):
        if len(cls.select(con, condition=condition)) == 0:
            print('no data found to change')
            return
        table_name = cls.__name__.lower()
        sql = f'UPDATE {table_name} SET '
        sql += new_vals
        sql += f' WHERE {condition};'
        cur = con.cursor()
        try:
            cur.execute(sql)
            print('changes were succesfully made')
        except sqlite3.Error as err:
            print(err)

    @classmethod
    def join(cls, con, cls2):
        if 'fk' in cls.__dict__:
            if cls.__dict__['fk'][1].table == cls2.__name__:
                sql = f'SELECT * ' \
                    f'FROM {cls.__name__} ' \
                    f'JOIN {cls2.__name__} on {cls2.__name__}.{cls.__dict__["fk"][1].name} = ' \
                    f'{cls.__name__}.{cls.__dict__["fk"][0]};'
            else:
                return 'unable to join tables wrong foreign key'

        elif 'fk' in cls2.__dict__:
            if cls2.__dict__['fk'][1].table == cls.__name__:
                sql = f'SELECT * ' \
                    f'FROM {cls2.__name__} ' \
                    f'JOIN {cls.__name__} on {cls.__name__}.{cls2.__dict__["fk"][1].name} = ' \
                    f'{cls2.__name__}.{cls2.__dict__["fk"][0]};'
            else:
                return 'unable to join tables wrong foreign key'
        else:
            return 'unable to join tables without foreign key'

        cur = con.cursor()
        try:
            cur.execute(sql)
            return cur.fetchall()
        except sqlite3.Error as err:
            print(err)