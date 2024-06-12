
from models.__init__ import CURSOR, CONN
from models.alcohol import Alcohol

class Supplier:
    all = {}

    def __init__(self, name, contact, id=None):
        self.id = id
        self.name = name
        self.contact = contact

    def __repr__(self):
        return f"<Supplier {self.id}: {self.name}, Contact: {self.contact}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        if isinstance(value, str) and len(value):
            self._contact = value
        else:
            raise ValueError("Contact must be a non-empty string")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                contact TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS suppliers"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO suppliers (name, contact) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.contact))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, contact):
        supplier = cls(name, contact)
        supplier.save()
        return supplier

    def update(self):
        sql = "UPDATE suppliers SET name = ?, contact = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.contact, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM suppliers WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM suppliers WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM suppliers WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        supplier = cls.all.get(row[0])
        if supplier:
            supplier.name = row[1]
            supplier.contact = row[2]
        else:
            supplier = cls(row[1], row[2])
            supplier.id = row[0]
            cls.all[supplier.id] = supplier
        return supplier

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM suppliers"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def get_alcohols(self):
        sql = "SELECT * FROM alcohol WHERE supplier_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Alcohol.instance_from_db(row) for row in rows]
