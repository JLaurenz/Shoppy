from seller import *
from product import *
from buyer import *
from cart import *

while(True):
    print("Welcome to LAPERA Online Shopping!")
    print("[1] Register Seller")
    print("[2] Register Buyer")
    print("[3] Login Seller")
    print("[4] Login Buyer")
    print("[5] View 5 Random Products")
    print("[q] Exit")
    choice = input("Enter choice:")
    if(choice == "1"):
        seller_init()
        seller_view_register()
    elif(choice == "2"):
        buyer_init()
        buyer_view_register()
        
    elif(choice == "3"):
        seller_view_login()
    elif(choice == "4"):
        buyer_view_login()
    elif(choice == "5"):
        product_view_random()

