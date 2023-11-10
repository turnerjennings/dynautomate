import numpy as np
import re


#function to find all keywords of a given type
#return: array of the first index of the given keyword at all locations it appears
def FindKeyword(key_file,key_title):
    start_index=[]
    search_term=re.compile(r'\*'+key_title) #define the re search term
    matches=search_term.finditer(key_file) #find all matching locations in the string
    for match in matches:
        start_index.append(match.start())
    return start_index
    

#function ot extract the string of a keyword given its start location
#return: string representing the total contents of a keyword file
def ReturnKeyword(key_file, key_locations, key_start):
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

            case "short":
                raise ValueError("Short keyfile format not supported yet\n")
            
            case "long":
                raise ValueError("Long keyfile format not supported yet\n")
            
            case __:
                raise ValueError("Unknown keyfile type\n")

k=KeywordFile("test_keyword.k","fixed")
