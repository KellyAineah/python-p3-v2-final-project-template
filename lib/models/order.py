from models.__init__ import CURSOR, CONN

class Order:
    all = {}

    def __init__(self, customer_id, alcohol_id, quantity, id=None):
        self.id = id
        self.customer_id = customer_id
        self.alcohol_id = alcohol_id
        self.quantity = quantity

    def __repr__(self):
        return f"<Order {self.id}: Customer {self.customer_id}, Alcohol {self.alcohol_id}, Quantity: {self.quantity}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                alcohol_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (customer_id) REFERENCES customers(id),
                FOREIGN KEY (alcohol_id) REFERENCES alcohol(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS orders"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = "INSERT INTO orders (customer_id, alcohol_id, quantity) VALUES (?, ?, ?)"
        CURSOR.execute(sql, (self.customer_id, self.alcohol_id, self.quantity))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, customer_id, alcohol_id, quantity):
        order = cls(customer_id, alcohol_id, quantity)
        order.save()
        return order

    def update(self):
        sql = "UPDATE orders SET customer_id = ?, alcohol_id = ?, quantity = ? WHERE id = ?"
        CURSOR.execute(sql, (self.customer_id, self.alcohol_id, self.quantity, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM orders WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM orders WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def instance_from_db(cls, row):
        order = cls.all.get(row[0])
        if order:
            order.customer_id = row[1]
            order.alcohol_id = row[2]
            order.quantity = row[3]
        else:
            order = cls(row[1], row[2], row[3])
            order.id = row[0]
            cls.all[order.id] = order
        return order

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM orders"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_customer(cls, customer_id):
        sql = "SELECT * FROM orders WHERE customer_id = ?"
        rows = CURSOR.execute(sql, (customer_id,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_alcohol(cls, alcohol_id):
        sql = "SELECT * FROM orders WHERE alcohol_id = ?"
        rows = CURSOR.execute(sql, (alcohol_id,)).fetchall()
        return [cls.instance_from_db(row) for row in rows]
