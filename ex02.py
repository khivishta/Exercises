# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 10:49:13 2020

@author: Khivishta
"""

def check_input_valid (userInput):
    return userInput=="<" or userInput=="="or userInput==">"

print("Think of a number between 1 and 100!")

minguess=1
maxguess=100
count=0

while minguess!=maxguess:
    
    middlenumber=int(minguess+(maxguess-minguess)/2)  
    
    print("Is your number greater (>), equal (=), or less (<) than" ,middlenumber,"?")
    sign=input("Please answer <, =, >!: ")
    
    while not check_input_valid(sign):
        sign=input("Wrong, Please answer <, =, >! ")
        
    if sign=="<":
        if middlenumber<=minguess:
            print("Error,you are lying")
        else:
            maxguess=middlenumber-1
            count=count+1 
            
    elif sign==">":
            minguess=middlenumber+1
            count=count+1 
        
    elif sign=="=":
        minguess=middlenumber
        maxguess=middlenumber
        count=count+1 
        
    if minguess==maxguess:
        print("your number is ", minguess)
        print("You needed" ,count,"steps")
