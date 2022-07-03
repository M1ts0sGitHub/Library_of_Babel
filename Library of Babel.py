#Library of Babel (Greeklish edition) in python by Dimitrios Alexandropoulos

import numpy as np
import unicodedata
from termcolor import colored
import os
import pyperclip
import time
import keyboard

# import sys
# Under development 
# if len(sys.argv) > 0:
#     for i in range(1, len(sys.argv)):
#         print(sys.argv[i])

pagesize = 1100
pageline= 55
pagepos= 0
validchars=("ABGDEZ8IKLMN0PRSTUFX1234567 9,.!") #Valid characters for Greeklish version + numbers

bin2enc={} 
for x in range(95): #binary to 7bits characters
    bin2enc["0" *(7-len(bin(x)[2:])) +bin(x)[2:]]=chr(x+32)
for x in range(192,225):
    bin2enc["0" *(7-len(bin(x-97)[2:])) +bin(x-97)[2:]]=chr(x)

enc2bin={}
for x in range(95): #7bits characters to binary
    enc2bin[chr(x+32)]= "0" *(7-len(bin(x)[2:])) +bin(x)[2:]
for x in range(192,225):
    enc2bin[chr(x)]= "0" *(7-len(bin(x-97)[2:])) +bin(x-97)[2:]

chars="" #valid 7bits characters
for x in range(len(bin2enc)):
    chars= chars + bin2enc["0" *(7-len(bin(x)[2:])) +bin(x)[2:]]

# Functions
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
def correct(text):
    temp=""
    for t in text:
        x = validchars.find(t)
        if x >= 0:
            temp = temp + t
    return temp
def greeklish(text):
    temp=""
    text=text.upper()
    alphabet = {
    "Α":"A", "Β":"B", "Γ":"G", "Δ":"D", "Ε":"E", "Ζ":"Z", "Η":"I", "Θ":"8", "Ι":"I", "Κ":"K", "Λ":"L", "Μ":"M",
    "Ν":"N", "Ξ":"KS", "Ο":"0", "Π":"P", "Ρ":"R", "Σ":"S", "Τ":"T", "Υ":"U", "Φ":"F", "Χ":"X", "Ψ":"PS", "Ω":"0" }
    for x in range(len(text)):
        if text[x] in alphabet:
            temp = temp + alphabet[text[x]]
        else:
            temp  = temp + text[x]
    return temp
def text2num(text):
    temp=0
    for x in range(len(text)):
        temp = temp + ord(text[x])
    return temp
def createpage(text):
    page=""
    temp=""
    rng= np.random.default_rng(text2num(text))
    pagepos=int(rng.random(1)*pagesize-len(text))
    # pagepos=0
    # print(pagepos)
    for x in range(pagesize-len(text)):
        page= page+validchars[int(rng.random(1)*len(validchars))]
    page = page[:pagepos] + text +page[pagepos:]
    return page
def printpage(page,text,f):
    if f==0:
        pagepos = page.find(text)
        for x in range(int(pagesize/pageline)):
            if (pagepos-pageline*(x))* (pagepos-pageline*(x+1))<0:
                print(colored("->","red"),page[pageline*(x):pageline*(x+1)])
            else:
                print("  ", page[pageline*(x):pageline*(x+1)])
        if text[:5] == "/page": 
            print("   " + " " *pageline + text[5:])
    else:
        f = open("page.txt", "w")
        for x in range(int(pagesize/pageline)):
            f.write(page[pageline*(x):pageline*(x+1)]+"\n")
        f.close()
def printaddress(address,f):
    if f == 0:
        for x in range(int(len(address)/pageline)):
            print("   " + address[pageline*x:pageline*(x+1)])
        print( "   " + address[pageline*(x+1):len(address)])
    else:
        f = open("address.txt", "w")
        for x in range(int(pagesize/pageline)):
            f.write(address[pageline*x:pageline*(x+1)]+"\n")
        f.write(address[pageline*(x+1):len(address)])
        f.close()
def bpage(page): # Convert page to binary
    temp =""
    dec2bin={}
    for x in range(32):
        dec2bin[validchars[x]]=  "0" *(5-len(bin(x)[2:])) +bin(x)[2:]
    # print(dec2bin)
    # print(len(page))
    for x in range(len(page)):
        temp = temp + dec2bin[page[x]]
    return temp
def hex2binary(hex): # Convert binary page to page
    temp =""
    enc2bin={}
    for x in range(95):
        enc2bin[chr(x+32)]= "0" *(7-len(bin(x)[2:])) +bin(x)[2:]
    for x in range(192,225):
        enc2bin[chr(x)]= "0" *(7-len(bin(x-97)[2:])) +bin(x-97)[2:]

    binary = ""
    for x in hex:
        binary = binary + str(enc2bin[x])
    return binary
def findaddress(page): # Finds page in Hex, wall, shelf, volume, page
    temp=""
    binpage = bpage(page)
    
    while len(binpage)>19:
        temp = temp + bin2enc[binpage[:7]]
        binpage = binpage[7:]
    
    hex, wall, shelf, volume, page = "",0,0,0,0
    wall = int(str(binpage[0:2]),2)+1
    shelf = int(str(binpage[2:5]),2)+1
    volume = int(str(binpage[5:10]),2)+1
    page = int(str(binpage[10:19]),2)+1
    hex  = enc(temp,str(page))
    address = hex+"-w"+str(wall)+"-s"+str(shelf)+"-v"+str(volume)+"-p"+str(page)
    
    return address
def address2page(address,offset):  #prints the address
    walln = address[783:].find("-w")+2 + 783
    shelfn = address[783:].find("-s")+2 + 783
    volumen = address[783:].find("-v")+2 + 783
    pagen = address[783:].find("-p")+2 + 783
    
    
    hex= address[:walln-2]
    wall = int(address[walln:shelfn-2])
    shelf = int(address[shelfn:volumen-2])
    volume = int(address[volumen:pagen-2])
    page = int(address[pagen:]) + offset
    
    hex= dec(hex,str(page))
    
    wallb = "{0:b}".format(int(wall-1))
    shelfb = "{0:b}".format(int(shelf-1))
    volumeb = "{0:b}".format(int(volume-1))
    pageb = "{0:b}".format(int(page-1))
    
    wallb = "0"*(2-len(wallb)) + wallb
    shelfb = "0"*(3-len(shelfb)) + shelfb
    volumeb = "0"*(5-len(volumeb)) + volumeb
    pageb = "0"*(9-len(pageb)) + pageb
        
    temp=""
    binary = hex2binary(hex) + wallb + shelfb + volumeb + pageb
    
    bin2dec={}
    for x in range(32):
        bin2dec["0" *(5-len(bin(x)[2:])) +bin(x)[2:]] = validchars[x]
    for x in range(0,len(binary),5):
        temp = temp + bin2dec[binary[x:x+5]]
    return temp 

def shuffle(text,seed):
    temp=[]
    rng= np.random.default_rng(text2num(seed))
    for i in range(len(text)):
        pos = int(rng.random(1)*len(text))
        temp.append(text[pos])
        text = text[:pos] + text[pos+1:]
    return temp
def enc(text,password):
    temp=""
    matrix=[]
    for i in range(len(text)):
        matrix.append(shuffle(chars,password+str(i)))
    # print(matrix)
    # print(validchars)
    for i in range(len(text)):
        # print(validchars.find(text[i]))
        temp = temp + matrix[i][chars.find(text[i])]
    return temp
def dec(text,password):
    temp=""
    matrix=[]
    for i in range(len(text)):
        matrix.append(shuffle(chars,password+str(i)))
    # print(matrix)
    # print(validchars)
    for i in range(len(text)):
        # print (chars[matrix[0].index(text[i])])
        temp = temp + chars[matrix[i].index(text[i])]
    return temp

ansstate=True
ans=""
os.system("title Library of Bable (alexandropoulos.dimitrios@gmail.com)")

while ansstate: #menu
    os.system("cls")
    print("Library of Babel (Greeklish Edition)")
    print()
    print("1.Browse the library")
    print("2.Search for a phrase (output to clipboard)")
    print("3.Search for a phrase (output to files)")
    print("4.Go to address, output to clipboard ")
    print()
    print("Give your choice: ", end ="")

    ans = input()
    if ans=="1":
        offset = 0 
        address = input("Address:> ")
        print()
        print("Page:")
        printpage(address2page(address,offset),"",0)
        print()        
        print("Use arrow keys to navigate through the volume or press esc")
        
        k=""
        while True:
            
            k = keyboard.read_key() 
            if k == "right" or k == "down":
                offset = offset +1
                print()
                print("Page:")
                printpage(address2page(address,offset),"/page"+str(int(address[address[783:].find("-p")+2+783:])+offset),0)
                print()
            elif k == "left" or k == "up":
                offset = offset -1
                print()
                print("Page:")
                printpage(address2page(address,offset),"/page"+str(int(address[address[783:].find("-p")+2+783:])+offset),0)
                print()
            elif keyboard.read_key() == "esc":
                break
        # ansstate = False
    elif ans=="2":
        print("Type in Greek")
        text = input("Search:> ")
        text= remove_accents(text)
        text = greeklish(text)
        text = correct(text)
        page = createpage(text)
        pyperclip.copy(page)
        print()
        print("Page:")
        printpage(page,text,0)
        print()
        address = ""
        address = findaddress(page)
        pyperclip.copy(address)
        print()
        print("Address:")
        printaddress(address,0)
        print()
        os.system("pause")
        # ansstate = False
    elif ans == "3":
        print("Type in Greek")
        text = input("Search:> ")
        text= remove_accents(text)
        text = greeklish(text)
        text = correct(text)
        page = createpage(text)
        printpage(page,text,1)
        address = ""
        address = findaddress(page)
        printaddress(address,1)
        os.system("pause")
        # ansstate = False
    elif ans == "4":
        address = input("Address:> ")
        print()
        print("Page:")
        page= address2page(address,0)
        printpage(page,"",0)
        pyperclip.copy(page)
        print()
        os.system("pause")
        # ansstate = False        
    else:
        if ans == "" :
            os.system("cls")
            break
        print()
        print("Input error! Try a number between 1 and 4 (1, 2, 3 & 4)")
        time.sleep(2)
