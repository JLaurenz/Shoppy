import getpass, os, hashlib, random
from globals import *

def product_create_dict( product_id,
                        product_seller_id,
                        product_category,
                        product_name,
                        product_description,
                        product_quantity,
                        product_unit_price
                    ):
    """Creates a dictionary from individual items.
    This is a helper function useful after reading 
    items from product.db
    """

    #create an emptry dictionary
    new_product_dict = {}

    #populate the fields
    new_product_dict["product_id"] = product_id
    new_product_dict["product_seller_id"] = product_seller_id
    new_product_dict["product_category"] = product_category
    new_product_dict["product_name"] = product_name
    new_product_dict["product_description"] = product_description
    new_product_dict["product_quantity"] = product_quantity
    new_product_dict["product_unit_price"] = product_unit_price
    
    #return the newly created and populated dictionary
    return new_product_dict

def product_load_db():
    """Reads the contents of product.db
    The contents are placed in the products
    global variable defined in globals.py
    """
    #we are using the global variable
    global  products

    #open the file for reading
    product_db_handle = open("data/product.db","r")
    #read all the lines 
    lines = product_db_handle.readlines()
    
    #remove existing items in the products list
    products.clear()

    #initialize the count to zero
    count = 0
    for line in lines:
        count += 1        
        fields = line.strip().split(",")
        
        #we call product_create_dict() to construct
        #a dictionary for us using the fields read 
        #from the file. This dictionary is appended
        #to the global 'products' variable
        products.append(product_create_dict(  fields[0],
                                            fields[1],
                                            fields[2],
                                            fields[3],
                                            fields[4],
                                            fields[5],
                                            fields[6]
                                              ))
    #close the handle 
    product_db_handle.close()

def product_init():
    """Initializes the product module. 
    It creates the product.db if it is absent 
    then calls product_load_db().
    """

    if not os.path.exists("data/product.db"):
        product_db_handle = open("data/product.db","w")
        product_db_handle.close()
    product_load_db()

def product_save_dict(product_dict):
    """Saves a dictionary of a product to product.db.
    """

    product_db_handle = open("data/product.db","a+")
    
    #construct the output line
    output_line = str(product_dict["product_id"]+","+
                    product_dict["product_seller_id"]+","+
                    product_dict["product_category"]+","+ 
                    product_dict["product_name"]+","+ 
                    product_dict["product_description"]+","+ 
                    product_dict["product_quantity"]+","+ 
                    product_dict["product_unit_price"]+"\n") 

    #write to file then close the handle
    product_db_handle.write(output_line)
    product_db_handle.close()

#return a dictionary with the product_category as key
def product_get_categories():
    """Returns a dictionary of product_category as key.
    """
    #we are using the global variable
    global  products
    #return product_category as key
    return {product_dict["product_category"]:product_dict["product_id"] for product_dict in products}

#product search
def product_search(search_term):
    """Searchs for a product.
    """
    #load the product.db
    product_load_db()
    #we are using the global variable
    global  products
    #create search_results
    product_search_dict = {}
    #search for the product using the product_name key, product_category key, and product_description key in a loop
    for product_dict in products:
        if search_term.lower() in product_dict["product_category"].lower() or search_term.lower() in product_dict["product_name"].lower() or search_term.lower() in product_dict["product_description"].lower():
            #add all the matching products to the search_results dictionary
            product_search_dict[product_dict["product_id"]] = product_dict
    #return the search_results dictionary
    return product_search_dict

def product_view_search():
    """Searchs for a product.
    """
    #we are using the global variable
    global  products
    
    #enter search term
    product_search_term = input("Keyword: ")
    #use product_search() to search for products and store the value
    product_search_dict = product_search(product_search_term)
    #count the number of search results and print 
    print(str(len(product_search_dict))+" match(es) found")
    #print the search results
    for key, product_search_results in product_search_dict.items():
        #print product id
        print(" [ " + str(key)+" ] - "+ str(product_search_results["product_name"]) + " , "+str(product_search_results["product_category"]) + " , "+ str(product_search_results["product_description"]) + " , "+str(product_search_results["product_unit_price"])+" per unit, "+str(product_search_results["product_quantity"])+" unit(s)")        
    
    input("Press [ENTER] to continue..")
    return product_search_dict

def product_flush_to_file():
    product_db_handle = open("data/product.db","w")

    for product_dict in products:
        output_line = str(product_dict["product_id"]+","+
                    product_dict["product_seller_id"]+","+
                    product_dict["product_category"]+","+
                    product_dict["product_name"]+","+
                    product_dict["product_description"]+","+
                    product_dict["product_quantity"]+","+
                    product_dict["product_unit_price"]+"\n")
        product_db_handle.write(output_line)
    product_db_handle.close()

#display random 5 products
def product_view_random():
    #we are using the global variable
    #load product databes
    product_load_db()
    global  products
    #check if products is less than 5
    #check if products is empty
    if len(products) == 0:
        print("No products available")
    elif len(products) < 5:
        #print the products
        for product_dict in products:
            print("[ "+ str(product_dict["product_id"])+" ] - "+ str(product_dict["product_name"]) + " , "+str(product_dict["product_category"]) + " , "+ str(product_dict["product_description"]) + " , "+str(product_dict["product_unit_price"])+" per unit, "+str(product_dict["product_quantity"])+" unit(s)")
    else:
        #randomly select 5 products
        random_products = random.sample(products,5)
        #print the products
        for random_product in random_products:
            print("[ "+ str(random_product["product_id"])+" ] - "+ str(random_product["product_name"]) + " , "+str(random_product["product_category"]) + " , "+ str(random_product["product_description"]) + " , "+str(random_product["product_unit_price"])+" per unit, "+str(random_product["product_quantity"])+" unit(s)")
    input("Press [ENTER] to continue..")
