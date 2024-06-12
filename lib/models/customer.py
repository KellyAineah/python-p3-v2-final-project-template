from models.__init__ import CURSOR, CONN

class Customer:
    all = {}

    def __init__(self, name, email, id=None):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<Customer {self.id}: {self.name}, Email: {self.email}>"

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
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if isinstance(value, str) and len(value):
            self._email = value
        else:
            raise ValueError("Email must be a non-empty string")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS customers"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO customers (name, email) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.email))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, email):
        customer = cls(name, email)
        customer.save()
        return customer

    def update(self):
        sql = "UPDATE customers SET name = ?, email = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.email, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM customers WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM customers WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM customers WHERE name = ?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        customer = cls.all.get(row[0])
        if customer:
            customer.name = row[1]
            customer.email = row[2]
        else:
            customer = cls(row[1], row[2])
            customer.id = row[0]
            cls.all[customer.id] = customer
        return customer

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM customers"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def get_orders(self):
        from models.order import Order 
        sql = "SELECT * FROM orders WHERE customer_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Order.instance_from_db(row) for row in rows]
