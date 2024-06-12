from models.alcohol import Alcohol
from models.supplier import Supplier
from models.customer import Customer
from models.order import Order

def exit_program():
    print("Goodbye!")
    exit(0)

def list_alcohol():
    alcohol_list = Alcohol.get_all()
    for alcohol in alcohol_list:
        print(f"{alcohol.id}: {alcohol.name}, {alcohol.type}, Supplier ID: {alcohol.supplier_id}, Price: {alcohol.price}")

def find_alcohol_by_name():
    name = input("Enter the alcohol's name: ")
    alcohol = Alcohol.find_by_name(name)
    if alcohol:
        print(f"{alcohol.id}: {alcohol.name}, {alcohol.type}, Supplier ID: {alcohol.supplier_id}, Price: {alcohol.price}")
    else:
        print(f'Alcohol {name} not found')

def find_alcohol_by_id():
    id_ = input("Enter the alcohol's id: ")
    alcohol = Alcohol.find_by_id(id_)
    if alcohol:
        print(f"{alcohol.id}: {alcohol.name}, {alcohol.type}, Supplier ID: {alcohol.supplier_id}, Price: {alcohol.price}")
    else:
        print(f'Alcohol {id_} not found')

def create_alcohol():
    name = input("Enter the alcohol's name: ")
    type_ = input("Enter the alcohol's type: ")
    supplier_id = input("Enter the supplier's id: ")
    price = input("Enter the alcohol's price: ")
    try:
        supplier_id = int(supplier_id)  
        Alcohol.create(name, type_, supplier_id, float(price))
        print(f'Successfully created alcohol {name}')
    except Exception as exc:
        print("Error creating alcohol: ", exc)

def update_alcohol():
    id_ = input("Enter the alcohol's id: ")
    alcohol = Alcohol.find_by_id(id_)
    if alcohol:
        name = input(f"Enter the new name (current: {alcohol.name}): ")
        type_ = input(f"Enter the new type (current: {alcohol.type}): ")
        supplier_id = input(f"Enter the new supplier id (current: {alcohol.supplier_id}): ")
        price = input(f"Enter the new price (current: {alcohol.price}): ")
        try:
            alcohol.name = name
            alcohol.type = type_
            alcohol.supplier_id = int(supplier_id)
            alcohol.price = float(price)
            alcohol.update()
            print(f'Successfully updated alcohol {alcohol.name}')
        except Exception as exc:
            print("Error updating alcohol: ", exc)
    else:
        print(f'Alcohol {id_} not found')

def delete_alcohol():
    id_ = input("Enter the alcohol's id: ")
    alcohol = Alcohol.find_by_id(id_)
    if alcohol:
        try:
            alcohol.delete()
            print(f'Successfully deleted alcohol {alcohol.name}')
        except Exception as exc:
            print("Error deleting alcohol: ", exc)
    else:
        print(f'Alcohol {id_} not found')

def list_suppliers():
    suppliers = Supplier.get_all()
    for supplier in suppliers:
        print(f"{supplier.id}: {supplier.name}, Contact: {supplier.contact}")

def find_supplier_by_name():
    name = input("Enter the supplier's name: ")
    supplier = Supplier.find_by_name(name)
    if supplier:
        print(f"{supplier.id}: {supplier.name}, Contact: {supplier.contact}")
    else:
        print(f'Supplier {name} not found')

def find_supplier_by_id():
    id_ = input("Enter the supplier's id: ")
    supplier = Supplier.find_by_id(id_)
    if supplier:
        print(f"{supplier.id}: {supplier.name}, Contact: {supplier.contact}")
    else:
        print(f'Supplier {id_} not found')

def create_supplier():
    name = input("Enter the supplier's name: ")
    contact = input("Enter the supplier's contact: ")
    try:
        Supplier.create(name, contact)
        print(f'Successfully created supplier {name}')
    except Exception as exc:
        print("Error creating supplier: ", exc)

def update_supplier():
    id_ = input("Enter the supplier's id: ")
    supplier = Supplier.find_by_id(id_)
    if supplier:
        name = input(f"Enter the new name (current: {supplier.name}): ")
        contact = input(f"Enter the new contact (current: {supplier.contact}): ")
        try:
            supplier.name = name
            supplier.contact = contact
            supplier.update()
            print(f'Successfully updated supplier {supplier.name}')
        except Exception as exc:
            print("Error updating supplier: ", exc)
    else:
        print(f'Supplier {id_} not found')

def delete_supplier():
    id_ = input("Enter the supplier's id: ")
    supplier = Supplier.find_by_id(id_)
    if supplier:
        try:
            supplier.delete()
            print(f'Successfully deleted supplier {supplier.name}')
        except Exception as exc:
            print("Error deleting supplier: ", exc)
    else:
        print(f'Supplier {id_} not found')


def view_alcohols_by_supplier():
    supplier_id = input("Enter the supplier's id: ")
    supplier = Supplier.find_by_id(int(supplier_id))
    if supplier:
        alcohols = supplier.get_alcohols()
        if alcohols:
            for alcohol in alcohols:
                print(f"{alcohol.id}: {alcohol.name}, {alcohol.type}, Price: {alcohol.price}")
        else:
            print(f'No alcohols found for supplier {supplier.name}')
    else:
        print(f'Supplier {supplier_id} not found')



def list_customers():
    customers = Customer.get_all()
    for customer in customers:
        print(f"{customer.id}: {customer.name}, Email: {customer.email}")

def find_customer_by_name():
    name = input("Enter the customer's name: ")
    customer = Customer.find_by_name(name)
    if customer:
        print(f"{customer.id}: {customer.name}, Email: {customer.email}")
    else:
        print(f'Customer {name} not found')

def find_customer_by_id():
    id_ = input("Enter the customer's id: ")
    customer = Customer.find_by_id(int(id_))
    if customer:
        print(f"{customer.id}: {customer.name}, Email: {customer.email}")
    else:
        print(f'Customer with id {id_} not found')

def create_customer():
    name = input("Enter the customer's name: ")
    email = input("Enter the customer's email: ")
    customer = Customer.create(name, email)
    print(f'Customer {customer.name} created with id {customer.id}')

def update_customer():
    id_ = input("Enter the customer's id: ")
    customer = Customer.find_by_id(int(id_))
    if customer:
        name = input(f"Enter new name for {customer.name} (press enter to skip): ")
        email = input(f"Enter new email for {customer.email} (press enter to skip): ")
        if name:
            customer.name = name
        if email:
            customer.email = email
        customer.update()
        print(f'Customer {customer.id} updated')
    else:
        print(f'Customer with id {id_} not found')

def delete_customer():
    id_ = input("Enter the customer's id: ")
    customer = Customer.find_by_id(int(id_))
    if customer:
        customer.delete()
        print(f'Customer {customer.id} deleted')
    else:
        print(f'Customer with id {id_} not found')

def create_order():
    customer_id = input("Enter the customer's id: ")
    alcohol_id = input("Enter the alcohol's id: ")
    quantity = input("Enter the quantity: ")
    order = Order.create(int(customer_id), int(alcohol_id), int(quantity))
    print(f'Order created with id {order.id}')

def view_orders_by_customer():
    customer_id = input("Enter the customer's id: ")
    orders = Order.find_by_customer(int(customer_id))
    if orders:
        for order in orders:
            print(f"{order.id}: Alcohol {order.alcohol_id}, Quantity: {order.quantity}")
    else:
        print(f'No orders found for customer with id {customer_id}')

def view_orders_by_alcohol():
    alcohol_id = input("Enter the alcohol's id: ")
    orders = Order.find_by_alcohol(int(alcohol_id))
    if orders:
        for order in orders:
            print(f"{order.id}: Customer {order.customer_id}, Quantity: {order.quantity}")
    else:
        print(f'No orders found for alcohol with id {alcohol_id}')




