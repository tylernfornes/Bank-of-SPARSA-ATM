#!/usr/bin/env python
import string
import requests
import json
import sys
import getpass
import os
import numbers

#url to connect to database
url = #insert Bank of SPARSA API server address here

#creates valid session from server
def getSession():
    args = {}
    args['accountNum'] = #INSERT ATM ACCOUNT HERE
    args['password'] = #INSERT ATM PASSWORD HERE
    loc = "/getSession"
    response = requests.post(url+loc,data=args)
    decodedOut = json.loads(response.text)
    session = None
    if isinstance(decodedOut, dict):
        return decodedOut['SessionID']
    else:
        print decodedOut

#grabs the current balance of the specific account
def getBalance(acct):
    args = {}
    session = getSession()
    args['accountNum'] = acct
    args['session'] = session
    loc = "/getBalance"
    response = requests.post(url+loc,data=args)
    decodedOut = json.loads(response.text)
    if isinstance(decodedOut, dict):
    	return decodedOut['Balance']
    else:
    	print decodedOut

#sends money to another sepcified account
def transferMoney(acct, amt, dest):
    args = {}
    session = getSession()
    args['accountNum'] = acct
    args['destAccount'] = dest
    args['session'] = session
    args['amount'] = amt
    loc = "/transferMoney"
    response = requests.post(url+loc,data=args)
    decodedOut = json.loads(response.text)
    if isinstance(decodedOut, list) and isinstance(decodedOut[0], dict):
    	print decodedOut[0]['Status']
        return True
    else:
        print decodedOut
        if "306" in decodedOut:
    	   print "CANNOT TRANSFER THAT AMOUNT, YOU'RE BROKE AS HELL"
        if "304" in decodedOut:
    	   print "INVALID DESTINATION ACCOUNT!"
        return False
#gets ping to authenticate account number
def getPin(acct):
    args = {}
    session = getSession()
    args['session'] = session
    args['accountNum'] = acct
    loc = "/getPin"
    response = requests.post(url+loc,data=args)
    try:
        decodedOut = json.loads(response.text)
    except ValueError, e:
            return "INVALID"
    if isinstance(decodedOut, dict):
        pin = decodedOut['Pin']
        return pin
    else:
        print decodedOut

#allows user to change account PIN associated with card
def changePIN(acct, old, new):
    args = {}
    session = getSession()
    args['accountNum'] = acct
    args['session'] = session
    args['newPin'] = new
    args['pin'] = old
    loc = "/changePin"
    response = requests.post(url+loc,data=args)
    decodedOut = json.loads(response.text)
    if isinstance(decodedOut, dict):
        print decodedOut['Status']
    else:
        if(decodedOut == "Error 801: We are unable to process your request"):
           print "\n"
    	   print "INVALID OR OLD PIN PROVIDED!"


################################################################################
keep_going = True
while keep_going:
	os.system("clear")
	try:
	    print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
	    print ("""\
	    $$$$$$$\                   $$\                       $$$$$$\         $$$$$$\ $$$$$$$\  $$$$$$\ $$$$$$$\  $$$$$$\  $$$$$$\\
	    $$  __$$\                  $$ |                     $$  __$$\       $$  __$$\$$  __$$\$$  __$$\$$  __$$\$$  __$$\$$  __$$\\
	    $$ |  $$ |$$$$$$\ $$$$$$$\ $$ |  $$\        $$$$$$\ $$ /  \__|      $$ /  \__$$ |  $$ $$ /  $$ $$ |  $$ $$ /  \__$$ /  $$ |
	    $$$$$$$\ |\____$$\$$  __$$\$$ | $$  |      $$  __$$\$$$$\           \$$$$$$\ $$$$$$$  $$$$$$$$ $$$$$$$  \$$$$$$\ $$$$$$$$ |
	    $$  __$$\ $$$$$$$ $$ |  $$ $$$$$$  /       $$ /  $$ $$  _|           \____$$\$$  ____/$$  __$$ $$  __$$< \____$$\$$  __$$ |
	    $$ |  $$ $$  __$$ $$ |  $$ $$  _$$<        $$ |  $$ $$ |            $$\   $$ $$ |     $$ |  $$ $$ |  $$ $$\   $$ $$ |  $$ |
	    $$$$$$$  \$$$$$$$ $$ |  $$ $$ | \$$\       \$$$$$$  $$ |            \$$$$$$  $$ |     $$ |  $$ $$ |  $$ \$$$$$$  $$ |  $$ |
	    \_______/ \_______\__|  \__\__|  \__|       \______/\__|             \______/\__|     \__|  \__\__|  \__|\______/\__|  \__|
	    """)
	    print "\n"

	    acctNum = str(getpass.getpass('Please swipe Bank of SPARSA card to begin: '))
	    acctNum = acctNum.translate(None, '%?')
	    if acctNum == "LUKE,IAMURFATHER":
	        print "bye bye"
	        keep_going = False
	        exit(0)
	    acctPIN = ''
	    tries = 3
	    while sum([1 if x.isdigit() else 0 for x in acctPIN])  != 4 and tries > 0:
		acctPIN = getpass.getpass('Enter PIN: ').strip()
		tries -= 1
	    print "\n"
	    pin = str(getPin(acctNum)).strip()
	    if pin == "INVALID":
		print "INVALID ACCOUNT/PIN COMBINATION! TRY AGAIN"

	    if acctPIN == pin:

		print "Welcome to Bank of SPARSA, please use the numberpad to select an option: \n"
		print "1: View Balance"
		print "2: Transfer Money"
		print "3: Change PIN \n"

		option = input("Enter option number: ")
		print "\n"

		if (option == 1):
		    balance  = getBalance(acctNum)
		    print ("Your current balance is: ${:,.2f}".format(balance))

		if (option == 2):
			try:
				amount = raw_input("Enter the amount to tranfer: $")
				amount = round(float(amount), 2)
				if amount > 0:
					destination = raw_input("Enter the destination account number: ")
					float(destination)
					print "\n"
					if not transferMoney(acctNum, amount, destination):
						print "Error transferring to that account."
				else:
					print "CANNOT TRANSFER NEGATIVE DOLLARS, DUH."
			except ValueError:
				print 'WHAT U TRYIN TO DO NOW, HUH?'

		if (option == 3):
			oldacctPIN = getpass.getpass("Enter current PIN: ")
			if oldacctPIN == acctPIN:
				tempacctPIN = getpass.getpass("Enter desired PIN: ")
				if tempacctPIN != acctPIN:
					if(len(tempacctPIN) == 4) and tempacctPIN.isdigit():
						newacctPIN = getpass.getpass("Confirm new PIN: ")
						if(tempacctPIN == newacctPIN):
							changePIN(acctNum, oldacctPIN, newacctPIN)
						else:
							print "NEW PINS DO NOT MATCH!"
					else:
						print 'NEW PIN MUST BE 4 CHARACTERS IN LENGTH'
				else:
					print "NEW ACCOUNT PIN CANNOT MATCH OLD PIN"

			else:
				print "INVALID ACCOUNT/PIN COMBINATION! TRY AGAIN"

	    print "\n"
	    raw_input("Press Enter to continue...")
	    os.system('clear')
	except:
		print "Hey now... none of that."
