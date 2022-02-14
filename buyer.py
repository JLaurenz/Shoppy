import getpass, os, hashlib

from globals import *
from product import *
from cart import *
from sale import *

def buyer_create_dict( buyer_id,
                        buyer_email,
                        buyer_first_name,
                        buyer_last_name,
                        buyer_password_hash
                    ):
    """Creates a dictionary from individual items.
    This is a helper function useful after reading 
    items from buyer.db
    """

    #create an emptry dictionary
    new_buyer_dict = {}

    #populate the fields
    new_buyer_dict["buyer_id"] = buyer_id
    new_buyer_dict["buyer_email"] = buyer_email
    new_buyer_dict["buyer_first_name"] = buyer_first_name
    new_buyer_dict["buyer_last_name"] = buyer_last_name 
    new_buyer_dict["buyer_password_hash"] = buyer_password_hash
    
    #return the newly created and populated dictionary
    return new_buyer_dict


def buyer_load_db():
    """Reads the contents of buyer.db
    The contents are placed in the buyers
    global variable defined in globals.py
    """
    #we are using the global variable
    global  buyers

    #open the file for reading
    buyer_db_handle = open("data/buyer.db","r")
    #read all the lines 
    lines = buyer_db_handle.readlines()
    
    #remove existing items in the buyers list
    buyers.clear()

    #initialize the count to zero
    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")
        
        #we call buyer_create_dict() to construct
        #a dictionary for us using the fields read 
        #from the file. This dictionary is appended
        #to the global 'buyers' variable
        buyers.append(buyer_create_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4]
                                              ))
    #close the handle 
    buyer_db_handle.close()


def buyer_init():
    """Initializes the buyer module. 
    It creates the buyer.db if it is absent 
    then calls buyer_load_db().
    """

    if not os.path.exists("data/buyer.db"):
        buyer_db_handle = open("data/buyer.db","w")
        buyer_db_handle.close()
    buyer_load_db()

def buyer_save_dict(buyer_dict):
    """Saves a dictionary of a buyer to buyer.db.
    """

    buyer_db_handle = open("data/buyer.db","a+")
    
    #construct the output line
    output_line = str(buyer_dict["buyer_id"]+","+
                    buyer_dict["buyer_email"]+","+
                    buyer_dict["buyer_first_name"]+","+ 
                    buyer_dict["buyer_last_name"]+","+ 
                    buyer_dict["buyer_password_hash"]+"\n") 

    #write to file then close the handle
    buyer_db_handle.write(output_line)
    buyer_db_handle.close()


def buyer_email_exists(email_to_check):
    """Check if the email exists. 
    We don't allow duplicate emails.
    Returns True if the email exists.
    """
    global buyers

    for buyer in buyers:
        if buyer["buyer_email"] == email_to_check:
            return True
    return False


def buyer_view_register():
    """buyer registration view.
    We follow the convention of having _view_ 
    in names of functions which require user
    interaction.
    """
    global buyers 

    print(">>[Register buyer]<<")
    
    new_buyer_dict = {}
    
    #the new buyer buyer_id will be +1 of the last 
    new_buyer_dict['buyer_id'] = str(len(buyers))
    
    #make sure no duplicate email will be used 
    #since it will be used in the login
    email=str(input("Email: "))
    while buyer_email_exists(email):
        print(email + " already exists! Please use another email")
        email=str(input("Email: "))

    #not a duplicate email so store in the dict    
    new_buyer_dict["buyer_email"] = email

    #obtain other buyer information
    new_buyer_dict["buyer_first_name"] = str(input("First Name: "))
    new_buyer_dict["buyer_last_name"] = str(input("Last Name: "))
    
    #For the password, it should not be displayed so we use the 
    #getpass package. We don't store the typed password. Instead 
    #we hash it and store the hash so that it is now visible. 
    #we compare the hash instead of the actual password
    #loop until the two passwords matched.
    matched = False
    while not matched:
        password_hash_1 = hashlib.sha256(getpass.getpass("Password: ").encode('utf-8')).hexdigest()
        password_hash_2 = hashlib.sha256(getpass.getpass("Retype Password: ").encode('utf-8')).hexdigest()
        #TODO: Make sure the password is not empty
        if password_hash_1 != password_hash_2:
            print("Password did not match! ")
        else:
            matched = True

    #store the hash of the password
    new_buyer_dict["buyer_password_hash"] = password_hash_1

    #save the new buyer 
    buyer_save_dict(new_buyer_dict)

    #reload the in-memory 'buyers' variable
    buyer_load_db()
    

def buyer_view_login():
    """Login view
    """
    #this global variable, defined in globals.py
    #stores the currently logged-in user
    global user_session
    #load database
    buyer_load_db()

    #email is the login name
    input_email = str(input("Email: "))

    #get and hash the password
    input_password_hash = hashlib.sha256(getpass.getpass("Password: ").encode('utf-8')).hexdigest()

    #initially set as false
    login_valid = False

    #we search for a matching email and password hash
    for buyer in buyers:
        if buyer["buyer_email"] == input_email:
            if buyer["buyer_password_hash"] == input_password_hash:
                login_valid = True
                break       #exit immediately since we found it
    
    #ok we're in
    if login_valid == True:
        print("\nWelcome " + buyer["buyer_first_name"] + "!" )

        #we use the buyer_id as the session_id
        session_id = buyer["buyer_id"];
        
        #we populate user_session
        user_session = {"session_id":session_id,"session_details":buyer}

        #show the options for the buyer
        buyer_view_menu()
    else:
        input("Unknown buyer! Press [ENTER] to continue.")


def buyer_view_add_product():
    """Allows to buyer to add a product.
    """
    global user_session

    new_product_dict = {}

    print(">>[Add Product]<<")

    new_product_dict['product_id'] = str(len(products))
    new_product_dict["product_buyer_id"] = user_session["session_id"]

    #Show a guide of existing categories, populate other fields
    print("Existing Categories:>> " + str(product_get_categories().keys()))
    new_product_dict["product_category"] = str(input("Category: "))
    new_product_dict["product_name"] = str(input("Product Name: "))
    new_product_dict["product_description"] = str(input("Product Description: "))
    new_product_dict["product_quantity"] = str(input("Quantity: "))
    new_product_dict["product_unit_price"] = str(input("Unit Price: "))
    
    #save and reload by calling the functions in
    #product.py
    product_save_dict(new_product_dict)
    product_load_db()


def buyer_view_menu():
    """The view for the buyer options.
    """

    choice = '8'
    while choice != 'q':
        print(">>[buyer Menu]<<")
        print("[1] Search/Add to Cart ")
        print("[2] View Cart ")
        print("[3] View Total Expenses ")
        print("[q] Exit ")
        choice = str(input("Enter choice: "))
        if choice == "1":
            buyer_view_search_product()
        elif choice == "2":
            #this is a function implemented in product.py
            product_view_search()   
        elif choice == "3":
            buyer_view_my_products()

#search product by name, category, and description
def buyer_view_search_product():
    """Search product by name, category, and description.
    """
    global products

    print(">>[Search Product]<<")
    #call product_view_search()
    product_view_search()
    input("Press [ENTER] to continue..")
    #Ask user to add to cart yes or no
    add_to_cart = str(input("Add to cart? (y/n): "))
    if add_to_cart == "y":
        product_id = str(input("Enter product id of item: "))
        quantity = str(input("How many units of the product? "))

    else:
        input("Press [ENTER] to continue..")
#buyer view cart
def buyer_view_my_products():
    """View cart
    """
    global user_session

    print(">>[View Cart]<<")

    #get the cart of the buyer
    cart = product_get_cart(user_session["session_id"])

    #show the cart
    for product in cart:
        print(product_to_string(product))

#view total expenses
def buyer_view_total_expenses():
    """View total expenses
    """
    global user_session

    print(">>[View Total Expenses]<<")

    #get the cart of the buyer
    cart = product_get_cart(user_session["session_id"])

    #calculate the total expenses
    total_expenses = 0
    for product in cart:
        total_expenses += int(product["product_quantity"]) * float(product["product_unit_price"])

    print("Total Expenses: " + str(total_expenses))
