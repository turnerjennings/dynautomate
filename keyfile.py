import numpy as np
import re


#function to find all keywords of a given type
#return: array of the first index of the given keyword at all locations it appears
def FindKeyword(key_file:str,key_title:str):
    start_index=[]
    search_term=re.compile(r'\*'+key_title) #define the re search term
    matches=search_term.finditer(key_file) #find all matching locations in the string
    for match in matches:
        start_index.append(match.start())
    return start_index
    

#function ot extract the string of a keyword given its start location
#return: string representing the total contents of a keyword file
def ReturnKeyword(key_file:str, key_locations:list, key_start:int) -> str:
    key_end=None
    for idx, val in enumerate(key_locations):
        if val > key_start:
            key_end=val
            break 
    if key_end is not None:
        keyword_match=key_file[key_start:key_end]
    else:
        keyword_match=key_file[key_start:]
    return keyword_match

#function to check if a number in a string is a float
#return: boolean
def is_float(s):
    try:
        float_value=float(s)
        return True
    except ValueError:
        return False

#define card object
class Card:

    def __init__(self,input_string:str,input_range:list[int],format:str):


        Card.string=input_string
        Card.format=format
        Card.range=input_range

        #extract length and values
        match format:

            case 'fixed': #if the card is space delimitted

                card_lines=input_string.split('\n')
                
                #check if there is a comment line or not
                if card_lines[0][0:2]=="$#":
                    card_lines.pop(0)
                
                card_values=card_lines[0].split()

                Card.length=len(card_values)

                #convert values to int or float
                for i,value in enumerate(card_values):

                    if value.isdigit()==True:

                        card_values[i]=int(value)

                    elif is_float(value)==True:

                        card_values[i]=float(value)

                    else:

                        raise ValueError("Card value at position " + i + " is not an integer or a float")
                    
                Card.values=card_values
                
            case 'short':
                card_lines=input_string.split('\n')
                
                #check if there is a comment line or not
                if card_lines[0][0:2]=="$#":
                    card_lines.pop(0)
                
                card_values=card_lines[0].split(',')

                Card.length=len(card_values)

                #convert values to int or float
                for i,value in enumerate(card_values):

                    if value.isdigit()==True:

                        card_values[i]=int(value)

                    elif is_float(value)==True:

                        card_values[i]=float(value)

                    else:

                        raise ValueError("Card value at position " + i + " is not an integer or a float")
                    
                Card.values=card_values

            #case for if the input isn't a fixed or a short
            case _:
                raise ValueError("Card format unexpected or unsupported")


    #method to print card info        
    def info(self):
        print("Card Format: " + str(Card.format) + "\nCard Range: " + str(Card.range) +
              "\nCard Length: " + str(Card.length) + "\nCard Values: " + str(Card.values) +
              "\nCard String: \n" + str(Card.string))

#define keyword file object
class KeywordFile:


    def __init__(self, path, type):

        #define keyword file object using inputs of the filepath to open and the data type ("fixed" or "short") 
        #check the given type to determine whether to interpret file via fixed width or via comma separation
        match type: 

            case "fixed":
                with open(path) as f:
                    keyfile_contents=f.read()

                #create an array of the location of every keyword in the file
                keyword_locations=[index for index,char in enumerate(keyfile_contents) if char=="*"]

                #extract the nodes of the keyword file
                nodes_location=FindKeyword(keyfile_contents,"NODE")
                nodes_string=ReturnKeyword(keyfile_contents,keyword_locations,nodes_location[0])
                
            case "short":
                raise ValueError("Short keyfile format not supported yet\n")
            
            case "long":
                raise ValueError("Long keyfile format not supported yet\n")
            
            case __:
                raise ValueError("Unknown keyfile type\n")

k=KeywordFile("test_keyword.k","fixed")
