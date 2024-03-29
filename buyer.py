import getpass, os, hashlib, datetime

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
    #laod buyer database for consitency
    buyer_load_db()
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


def buyer_view_menu():
    """The view for the buyer options.
    """

    choice = '8'
    while choice != 'q':
        print(">>[Buyer Menu]<<")
        print("[1] Search/Add to Cart ")
        print("[2] View Cart ")
        print("[3] View Total Expenses ")
        print("[q] Exit ")
        choice = str(input("Enter choice: "))
        if choice == "1":
            buyer_view_search_product()
        elif choice == "2":
            #this is a function implemented in product.py
            buyer_view_cart()   
        elif choice == "3":
            buyer_view_total_expenses()

#search product by name, category, and description
def buyer_view_search_product():
    """Search product by name, category, and description.
    """
    global products ,carts
    #load the product databases
    product_load_db()

    #create a new car_dict
    new_cart_dict = {}
    print(">>[SEARCH]<<")
    #call product_view_search() and save the return value into a dict
    buyer_search_result = product_view_search()
    #ask user to add to cart or not
    add_to_cart = str(input("Add to cart? (y/n): "))
    if add_to_cart == "y": #if yes
        new_cart_dict['cart_id'] = str(len(carts)) #compute the cart length and assign it to the cart_id
        new_cart_dict["cart_buyer_id"] = user_session["session_id"] #assign the buyer_id to the cart yung session id
        product_id = str(input("Enter product id of item: ")) #get the product id yung id nung product
        #check if product id to int is not in the product id of search result dictionary
        if product_id not in buyer_search_result:
            print("Product id not found!")
            return
        else: #dito pag tama id ng product continue
            new_cart_dict["cart_product_id"] = product_id
            quantity = str(input("How many units of the product? "))
            #access the product id and che4ck the qunatity
            for product in products: #babasahin yung product tapos hahanapin yung qunatity 
                if product["product_id"] == product_id:
                    if int(quantity) > int(product["product_quantity"]): #pag naman sobra yung ininput na quantity ni user babalik sa pinaka menu ulet
                        print("Not enough quantity!")
                        return
            else: #pag naman yung quantity na input na user ay mas mababa or sakto sa quantity  tutuloy
                new_cart_dict["cart_quantity"] = quantity #assign the quantity to the cart
                new_cart_dict["cart_checkedout"] = "0" #assign the cart_checkedout to 0 kasi pag naging 1 ibig sabihin checked out na ni user
                new_cart_dict["cart_date"] = str(datetime.datetime.now()) #sasave lang to ng date
        #save the new cart to cart 

        #change the product quantity in the product database
        for product in products: #loop ulet babasahin isa isa
            if product["product_id"] == product_id:
                product["product_quantity"] = str(int(product["product_quantity"]) - int(quantity)) #pag naman nahanap yung qunatity babawasang quantity sa product database
                break #pag end yung loop
        product_flush_to_file() # uulitin yung pag sasave ng product sa database
        #save the new cart to cart database
        cart_save_dict(new_cart_dict)
    else:
        input("Press [ENTER] to continue..") #pag ayaw mag add to cart ni user


def buyer_view_cart():
    """Show all the products of this user
    """
    product_load_db()
    cart_load_db()
    global products
    global carts
    global user_session
    i = 0;
    print("Listed below are your products: ")
    for cart in carts:
        if cart["cart_buyer_id"] == user_session["session_id"]:
            for product in products:
                if product["product_id"] == cart["cart_product_id"]:
                    i +=1
                    print(
                            " ["+cart["cart_product_id"]+"] - "+
                            product["product_name"]+" - "+
                            cart["cart_quantity"]+" unit(s)"
                        )
                    break
    if i == 0:
        print("No items in yout cart.")
        return
    print("There are "+str(i)+" items in your cart.")
    #checkout or not
    checkout = str(input("Checkout an Item [y/n]: "))

    if checkout == "y":

        checkout_item = str(input("Enter [Item ID] of item: "))
        #create a new sales dict and save it to sales
        new_sales_dict = {}

        new_sales_dict["sale_id"] = str(len(sales))
        new_sales_dict["sale_buyer_id"] = user_session["session_id"]
        new_sales_dict["sale_product_id"] = checkout_item
        new_sales_dict["sale_quantity"] = cart["cart_quantity"]
        new_sales_dict["sale_date"] = str(datetime.datetime.now())
        
        #count the total price
        total_price = 0
        for cart in carts:
            if cart["cart_buyer_id"] == user_session["session_id"]:
                for product in products:
                    if product["product_id"] == cart["cart_product_id"]:
                        total_price = (int(cart["cart_quantity"]) * int(product["product_unit_price"]))
                        break
        new_sales_dict["sale_total_amount"] = str(total_price)
        sale_save_dict(new_sales_dict)
        #change the cart_checkedout to 1
        for cart in carts:
            if cart["cart_buyer_id"] == user_session["session_id"]:
                cart["cart_checkedout"] = "1"
        cart_flush_to_file()
        print("Checkout successful!")
    else:
        input("Press [ENTER] to continue..")
        
#view total expenses
def buyer_view_total_expenses():
    """Compute the total sales for current logged in seller.
    """
    global sales
    global user_session
    #load sales database
    sale_load_db()
    #go over the "sales" global variable 
    # and check for items related to the current 
    # logged in user 
    buyer_view_total_expenses = 0;
    #look for the current logged in user
    for sale in sales:
        if sale["sale_buyer_id"] == user_session["session_id"]:
            buyer_view_total_expenses += int(sale["sale_total_amount"])    
    
    print("Your total expense: ", buyer_view_total_expenses)
    input("Press [ENTER] to continue..")
