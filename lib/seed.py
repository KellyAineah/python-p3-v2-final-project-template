#!/usr/bin/env python3

from models.__init__ import CONN, CURSOR
from models.alcohol import Alcohol
from models.supplier import Supplier
from models.customer import Customer
from models.order import Order

def seed_database():
    Alcohol.create_table()
    Supplier.create_table()
    Customer.create_table()
    Order.create_table()
   

seed_database()
print("Seeded database")
