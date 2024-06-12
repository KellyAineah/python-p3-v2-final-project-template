#!/usr/bin/python3

from helpers import (
    exit_program,
    list_alcohol,
    find_alcohol_by_name,
    find_alcohol_by_id,
    create_alcohol,
    update_alcohol,
    delete_alcohol,
    list_suppliers,
    find_supplier_by_name,
    find_supplier_by_id,
    create_supplier,
    update_supplier,
    delete_supplier,
    view_alcohols_by_supplier,
    list_customers,
    find_customer_by_name,
    find_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    create_order,
    view_orders_by_customer,
    view_orders_by_alcohol,
)

def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()

        elif choice == "1":
            list_suppliers()
        elif choice == "2":
            find_supplier_by_name()
        elif choice == "3":
            find_supplier_by_id()
        elif choice == "4":
            create_supplier()
        elif choice == "5":
            update_supplier()
        elif choice == "6":
            delete_supplier()

        elif choice == "7":
            list_alcohol()
        elif choice == "8":
            find_alcohol_by_name()
        elif choice == "9":
            find_alcohol_by_id()
        elif choice == "10":
            create_alcohol()
        elif choice == "11":
            update_alcohol()
        elif choice == "12":
            delete_alcohol()
        elif choice == "13":
            view_alcohols_by_supplier()

        elif choice == "14":
            list_customers()
        elif choice == "15":
            find_customer_by_name()
        elif choice == "16":
            find_customer_by_id()
        elif choice == "17":
            create_customer()
        elif choice == "18":
            update_customer()
        elif choice == "19":
            delete_customer()

        elif choice == "20":
            create_order()
        elif choice == "21":
            view_orders_by_customer()
        elif choice == "22":
            view_orders_by_alcohol()
        
        else:
            print("Invalid choice")

def menu():
    
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all suppliers")
    print("2. Find supplier by name")
    print("3. Find supplier by id")
    print("4. Create supplier")
    print("5. Update supplier")
    print("6. Delete supplier")
    print("7. List all alcohol")
    print("8. Find alcohol by name")
    print("9. Find alcohol by id")
    print("10. Create alcohol")
    print("11. Update alcohol")
    print("12. Delete alcohol")
    print("13. View alcohols by supplier")
    print("14. List all customers")
    print("15. Find customer by name")
    print("16. Find customer by id")
    print("17. Create customer")
    print("18. Update customer")
    print("19. Delete customer")
    print("20. Create order")
    print("21. View orders by customer")
    print("22. View orders by alcohol")
    

if __name__ == "__main__":
    main()
