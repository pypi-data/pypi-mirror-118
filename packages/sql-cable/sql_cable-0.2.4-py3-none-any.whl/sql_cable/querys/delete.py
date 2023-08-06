import sqlite3


class Delete:
    def __init__(self, model_in, table_name, db_path):
        self.model_in = model_in
        self.table_name = table_name
        self.db_path = db_path

    def remove(self, separator="AND", **kwargs):
        query = f"DELETE FROM {self.table_name} WHERE"
        params = []
        for column in kwargs:
            query += f"{column} = ?"
            params.append(kwargs[column])
        conn = sqlite3.connection(self.db_path)
        c = conn.cursor()
        c.execute(query, tuple(params))
        conn.commit()
        conn.close()
        self.model_in.load_querrys()
