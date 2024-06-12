from models.__init__ import CURSOR, CONN
from models.customer import Customer

class Alcohol:
    all = {}

    # Initialize object.
    def __init__(self, name, type_, supplier_id, price, id=None):
        self.id = id  
        self.name = name  
        self.type = type_  
        self.supplier_id = supplier_id  
        self.price = price  

    # String representation 
    def __repr__(self):
        return f"<Alcohol {self.id}: {self.name}, {self.type}, Supplier ID: {self.supplier_id}, Price: {self.price}>"

    # Getter and setter for the name property.
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value):
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")

    # Getter and setter for the type property.
    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if isinstance(value, str) and len(value):
            self._type = value
        else:
            raise ValueError("Type must be a non-empty string")

    # Getter and setter for the supplier_id property.
    @property
    def supplier_id(self):
        return self._supplier_id

    @supplier_id.setter
    def supplier_id(self, value):
        if isinstance(value, int):
            sql = "SELECT id FROM suppliers WHERE id = ?"
            supplier = CURSOR.execute(sql, (value,)).fetchone()
            if supplier:
                self._supplier_id = value
            else:
                raise ValueError("supplier_id must reference a supplier in the database")
        else:
            raise ValueError("supplier_id must be an integer")

    # Getter and setter for the price property.
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if isinstance(value, (int, float)) and value > 0:
            self._price = value
        else:
            raise ValueError("Price must be a positive number")

    # Class method to create the alcohol table in the database.
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Alcohol instances """
        
        sql = """
            CREATE TABLE IF NOT EXISTS alcohol (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            supplier_id INTEGER,
            price REAL,
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Class method to drop the alcohol table in the database.
    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Alcohol instances """
        sql = """
            DROP TABLE IF EXISTS alcohol;
        """
        CURSOR.execute(sql)
        CONN.commit()

    # Save the Alcohol object to the database.
    def save(self):
        """ Insert a new row with the name and location values of the current Alcohol instance.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        sql = """
            INSERT INTO alcohol (name, type, supplier_id, price)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.type, self.supplier_id, self.price))
        CONN.commit()
        self.id = CURSOR.lastrowid 
        type(self).all[self.id] = self  

    # Class method to create and save a new Alcohol object.
    @classmethod
    def create(cls, name, type_, supplier_id, price):
        """ Initialize a new Alcohol instance and save the object to the database """
        alcohol = cls(name, type_, supplier_id, price)
        alcohol.save()
        return alcohol

    # Update the Alcohol object in the database.
    def update(self):
        """Update the table row corresponding to the current Alcohol instance."""
        sql = """
            UPDATE alcohol
            SET name = ?, type = ?, supplier_id = ?, price = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.type, self.supplier_id, self.price, self.id))
        CONN.commit()

    # Delete the Alcohol object from the database.
    def delete(self):
        """Delete the table row corresponding to the current Alcohol instance,
        delete the dictionary entry, and reassign id attribute"""
        sql = """
            DELETE FROM alcohol
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id] 
        self.id = None 

    # Class method to find Alcohol object by its ID.
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM alcohol
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # Class method to find a Alcohol object by its name.
    @classmethod
    def find_by_name(cls, name):
        """Return a Alcohol object corresponding to first table row matching specified name"""
        sql = """
            SELECT * FROM alcohol
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # Create Alcohol object from a database row.
    @classmethod
    def instance_from_db(cls, row):
        """Return a Alcohol object having the attribute values from the table row."""
        alcohol = cls.all.get(row[0])  
        if alcohol:
            alcohol.name = row[1]
            alcohol.type = row[2]
            alcohol.supplier_id = row[3]
            alcohol.price = row[4]
        else:
            alcohol = cls(row[1], row[2], row[3], row[4])
            alcohol.id = row[0]
            cls.all[alcohol.id] = alcohol  
        return alcohol

    # Class method to get all Alcohol objects from the database.
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM alcohol
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    def suppliers(self):
        """Return list of suppliers associated with current alcohol"""
        from models.supplier import Supplier
        sql = """
            SELECT * FROM suppliers
            WHERE supplier_id = ?
        """
        CURSOR.execute(sql, (self.id,))

        rows = CURSOR.fetchall()
        return [
            Supplier.instance_from_db(row) for row in rows
        ]


    def get_customers(self):
        sql = "SELECT * FROM orders WHERE alcohol_id = ?"
        rows = CURSOR.execute(sql, (self.id,)).fetchall()
        return [Customer.instance_from_db(CURSOR.execute("SELECT * FROM customers WHERE id = ?", (row[1],)).fetchone()) for row in rows]

