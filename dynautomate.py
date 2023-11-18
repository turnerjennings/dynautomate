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

#function to find the nth comma in a comma separated list
#return: int
def find_nth_comma(input_string:str, n:int)->int:
    position = -1
    for _ in range(n):
        position = input_string.find(',', position + 1)
        if position == -1:
            break  # Break if the nth comma is not found
    return position

#define card object
class Card:

    def __init__(self,input_string:str,input_range:list[int],format:str):


        self.string=input_string
        self.format=format
        self.range=input_range

        #extract length and values
        match self.format:

            case 'fixed': #if the card is space delimitted

                card_lines=input_string.split('\n')
                
                #check if there is a comment line or not
                if card_lines[0][0:1]=="$":
                    self.comment=True
                    card_length=len(card_lines[0])
                    card_lines[1].ljust(card_length)
                    card_lines.pop(0)
                    
                else:
                    self.comment=False
                    card_length=len(card_lines[0])
                
                card_values=[card_lines[0][i:i+10] for i in range(0, card_length, 10)]

                self.length=len(card_values)

                #convert values to int or float
                for i,val in enumerate(card_values):
                    value=val.lstrip()
                    if value.isdigit()==True:

                        card_values[i]=int(value)

                    elif is_float(value)==True:

                        card_values[i]=float(value)

                    elif value=='':
                        card_values[i]='          '

                    else:

                        raise ValueError("Error parsing fixed card format: Card value at position " + str(i) + " is not an integer or a float")
                    
                self.values=card_values
                
            case 'short':
                card_lines=input_string.split('\n')
                
                #check if there is a comment line or not
                if card_lines[0][0:1]=="$":
                    self.comment=True
                    card_lines.pop(0)
                else:
                    self.comment=False
                
                card_values=card_lines[0].split(',')

                self.length=len(card_values)

                #convert values to int or float
                for i,value in enumerate(card_values):

                    if value.isdigit()==True:

                        card_values[i]=int(value)

                    elif is_float(value)==True:

                        card_values[i]=float(value)

                    elif value=='' or value.isspace()==True:
                        card_values[i]=''
                    else:

                        raise ValueError("Error parsing short card format: Card value at position " + str(i) + " is not an integer or a float")
                    
                self.values=card_values

            #case for if the input isn't a fixed or a short
            case _:
                raise ValueError("Card format unexpected or unsupported")
    
    #define object magic methods
    def __str__ (self): return f"Card(Number of values: {self.length}, Range: {self.range})"

    def __len__(self): return len(self.values)

    def __getitem__(self, key): return self.values[key]

    def __setitem__(self,key,value): self.edit(key,value)

    #method to print card info        
    def info(self):
        print("Card Format: " + str(self.format) + "\nCard comment included: " + str(self.comment) + 
              "\nCard Range: " + str(self.range) +
              "\nCard Length: " + str(self.length) + "\nCard Values: " + str(self.values) +
              "\nCard String: \n" + str(self.string))
        
    def edit(self,edit_index:int,edit_value):

        #check inputs
        if edit_index > self.length or edit_index < 0:
            raise IndexError("Value index out of range")


        #check write format
        match self.format:

            case "fixed":

                #check if the value being inserted is the same as the existing value
                if type(self.values[edit_index]) == type(edit_value) or self.values[edit_index]==0 or self.values[edit_index]=='          ':

                    #check if card has comment and adjust start location accordingly
                    if self.comment==True:
                        preceding_value_end=self.string.find('\n')+10*edit_index+1

                    elif self.comment==False:
                        preceding_value_end=10*edit_index

                    #find the end of the new value in the array
                    edit_value_end=preceding_value_end+10
        

                    #define the edit range and the value to be replaced
                    value_to_replace=self.string[preceding_value_end:edit_value_end]
                    edit_range=edit_value_end-preceding_value_end
                    
                    #print("Range: " + str([preceding_value_end,edit_value_end]) + "\nStart character: " + self.string[preceding_value_end] +
                    #      "\nEnd character: " + self.string[edit_value_end] + "\nFull string to be replaced: {" + str(value_to_replace) +"}")
                   
                    #edit the value in the array
                    self.values[edit_index]=edit_value
                    
                    #check if value is integer or float, write accordingly
                    if type(edit_value)==float:
                        new_string=self.string[0:preceding_value_end]+f"{edit_value:#.{edit_range-5}G}".rjust(10)+self.string[edit_value_end:]
                        self.string=new_string
                        
                        #Card.string=Card.string.replace(value_to_replace,f"{edit_value:#.{edit_range-5}G}")
                        

                    elif type(self.values[edit_index])==int:
                        new_string=self.string[0:preceding_value_end]+f"{edit_value:{edit_range}}"+self.string[edit_value_end:]
                        self.string=new_string
                        
                        #Card.string=Card.string.replace(value_to_replace,f"{edit_value:{edit_range}}")
                    
                    else:
                        raise ValueError("The value inserted in the keyword is not an int or a float")
                    #print("New Values: "+str(self.values)+"\nNew string: \n" + str(self.string))
                    

                else:
                    raise TypeError("Input value type does not match existing data type")
                
            case "short":
                #check if the value being inserted is the same as the existing value
                if type(self.values[edit_index]) == type(edit_value) or self.values[edit_index]==0 or self.values[edit_index]=='':

                    #check if card has comment and adjust start location accordingly
                    comma_location=find_nth_comma(self.string,edit_index)

                    #if there is no commas on the line to start
                    if comma_location < 0:
                        preceding_value_end=0
                        edit_value_end=1
                    else:
                        preceding_value_end=comma_location
                        edit_value_end=self.string.find(',',preceding_value_end+1)

                    #find the end of the new value in the array
                    
                    
        

                    #define the edit range and the value to be replaced
                    value_to_replace=self.string[preceding_value_end:edit_value_end]
                    
                    #print("Range: " + str([preceding_value_end,edit_value_end]) + "\nStart character: " + self.string[preceding_value_end] +
                    #      "\nEnd character: " + self.string[edit_value_end] + "\nFull string to be replaced: {" + str(value_to_replace) +"}")
                   
                    #edit the value in the array
                    self.values[edit_index]=edit_value
                    
                    #check if value is integer or float, write accordingly
                    if type(edit_value)==float:
                        if comma_location < 0:
                            new_string=self.string[0:preceding_value_end+1]+f"{edit_value:#.5G}"+','+self.string[edit_value_end:]
                        else:
                            new_string=self.string[0:preceding_value_end+1]+f"{edit_value:#.5G}"+self.string[edit_value_end:]
                        self.string=new_string
                                                

                    elif type(self.values[edit_index])==int:
                        if comma_location < 0:
                            new_string=self.string[0:preceding_value_end+1]+str(edit_value)+','+self.string[edit_value_end:]
                        else:
                            new_string=self.string[0:preceding_value_end+1]+str(edit_value)+self.string[edit_value_end:]
                        self.string=new_string
                        
                        #Card.string=Card.string.replace(value_to_replace,f"{edit_value:{edit_range}}")
                    
                    else:
                        raise ValueError("The value inserted in the keyword is not an int or a float")
                    print("New Values: "+str(self.values)+"\nNew string: \n" + str(self.string))
                    

                else:
                    raise TypeError("Input value type does not match existing data type")

            case "long": 
                
               #check if the value being inserted is the same as the existing value
                if type(self.values[edit_index]) == type(edit_value) or self.values[edit_index]==0:

                    #check if card has comment and adjust start location accordingly
                    if self.comment==True:
                        preceding_value_end=self.string.find('\n')+20*edit_index+1

                    elif self.comment==False:
                        preceding_value_end=20*edit_index+1

                    #find the end of the new value in the array
                    edit_value_end=preceding_value_end+20
        

                    #define the edit range and the value to be replaced
                    value_to_replace=self.string[preceding_value_end:edit_value_end]
                    edit_range=edit_value_end-preceding_value_end
                    
                    print("Range: " + str([preceding_value_end,edit_value_end]) + "\nStart character: " + self.string[preceding_value_end] +
                          "\nEnd character: " + self.string[edit_value_end] + "\nFull string to be replaced: {" + str(value_to_replace) +"}")
                   
                    #edit the value in the array
                    self.values[edit_index]=edit_value
                    
                    #check if value is integer or float, write accordingly
                    if type(edit_value)==float:
                        new_string=self.string[0:preceding_value_end]+f"{edit_value:#.{edit_range-5}G}".rjust(20)+self.string[edit_value_end:]
                        self.string=new_string
                        
                        #Card.string=Card.string.replace(value_to_replace,f"{edit_value:#.{edit_range-5}G}")
                        

                    elif type(self.values[edit_index])==int:
                        new_string=self.string[0:preceding_value_end]+f"{edit_value:{edit_range}}"+self.string[edit_value_end:]
                        self.string=new_string
                        
                        #Card.string=Card.string.replace(value_to_replace,f"{edit_value:{edit_range}}")
                    
                    else:
                        raise ValueError("The value inserted in the keyword is not an int or a float")
                    print("New Values: "+str(self.values)+"\nNew string: \n" + str(self.string))
                    

                else:
                    raise TypeError("Input value type does not match existing data type")

            case _:
                raise ValueError("Unknown card format")


class Keyword:

    def __init__(self,input_string:str,input_range:list[int],format:str):
        
        #initialize basic properties
        self.string=input_string
        self.format=format
        self.range=input_range
        self.cards=[]

        #check if the string contains comments and the title block
        end_first_line=input_string.find('\n')
        self.name=input_string[0:end_first_line]

        
        #for each line in the self, sort according to title, comment, and values
        range_count=0
        comment_line=None
        for i,line in enumerate(input_string.splitlines()):
            #check if the line is a comment, if so store it
            if line.find('$') >=0:
                comment_line=line

            #if the line is not a comment   
            elif line.find("*")<0:
                
                #check if the previous line was a comment
                if comment_line != None:
                    #if yes, add previous comment line to current comment line, the reset comment line
                    card_string=comment_line + "\n" + line
                    comment_line=None

                else:
                    #if no, set card string to current line
                    card_string=line

                #create a new card using the current line and append it to the array
                new_card=Card(card_string,[range_count,range_count+len(line)],self.format)
                self.cards.append(new_card)
            

                #update the start point of the next range
                range_count+=len(card_string)+1
            else:
                range_count+=len(line)+1
                
            
    
        #count the number of cards
        self.cardcount=len(self.cards)
    
    #method to print the keyword information
    def info(self):
        print("Keyword name: " + str(self.name) + "\nKeyword format: " + str(self.format) + 
              "\nKeyword range: " + str(self.range) + "\nKeyword card count: " + str(self.cardcount) + 
              "\nKeyword cards: \n" + str(self.cards) + "\nKeyword string: \n" + str(self.string))
        


    #define magic methods
    def __str__(self): return f"Keyword(Number of cards: {self.cardcount}, Range: {self.range})"
    
    def __len__(self): return self.cardcount

    def __getitem__(self, key): return self.cards[key]

    def __setitem__(self,key,value): self.edit_card(key,value)

    #method to retrieve a card from the list as a new object outside of the keyword    
    def get_card(self, card_num:int):
        return self.cards[card_num]
    

    #method to edit a card without retrieving it
    def edit_card(self,card_num,edit_index:int,edit_value):

        #edit the card object
        self.cards[card_num].edit(edit_index,edit_value)
        
        #define the string to be inserted into the keyword string
        new_card_string=str(self.cards[card_num].string)

        #define the range of indices to be replaced
        insert_range=self.cards[card_num].range
        
        #insert the values into the string
        new_keyword_string=self.string[:insert_range[0]]+new_card_string+self.string[insert_range[1]:]
        self.string=new_keyword_string
    

    #method to replace a card with a new card
    def replace_card(self,card_num,card_replace):
        self.cards[card_num]=card_replace
        
        #define the string to be inserted into the keyword string
        new_card_string=str(self.cards[card_num].string)

        #define the range of indices to be replaced
        insert_range=self.cards[card_num].range
        
        #insert the values into the string
        new_keyword_string=self.string[:insert_range[0]]+new_card_string+self.string[insert_range[1]:]
        self.string=new_keyword_string

    




#define keyword file object
class KeywordFile:


    def __init__(self, path:str, format:str):

        #define keyword file object using inputs of the filepath to open and the data type ("fixed" or "short") 
        #check the given type to determine whether to interpret file via fixed width or via comma separation
        
        
        #read contents of input file
        with open(path) as f:
            keyfile_contents=f.read()
        self.string=keyfile_contents
                
        #define object properties from inputs
        self.format=format
        self.path=path
        self.length=len(self.string)

        #create an array of the location of every keyword in the file
        indices=[]
        index = self.string.find("*")
        while index != -1:
            indices.append(index)
            index = self.string.find("*", index + 1)

        if len(indices)==0:
            raise Exception("No keywords found in file")
        
        self.keywordlocations=indices
        self.keywordcount=len(indices)
        
        #define keyword deck title
        if self.string[self.keywordlocations[1]+1:self.keywordlocations[1]+6]=="TITLE":
            self.title=self.string[self.keywordlocations[1]+7:self.keywordlocations[2]-1]
        else:
            self.title=None
            
    #initialize magic methods
    def __str__(self): return f"Keyword file (Title: {self.title} Number of keywords: {self.keywordcount})"
    
    def __len__(self): return self.keywordcount

    #def __getitem__(self, key): return self.cards[key]

    #def __setitem__(self,key,value): self.edit_card(key,value)
    
    def info(self):
        print(f"Keyword file\nTitle: {self.title}\nFile length: {self.length}\n" + 
              f"Number of keywords: {self.keywordcount}\nKeyword locations:\n {self.keywordlocations}\n")
    
    
    #function to return a list of all keywords of a type in the deck
    def get_keywords(self,keyword_title:str):
        title_length=len(keyword_title)
        keyword_list=[]
        
        #for each keyword location, 
        for idx,loc in enumerate(self.keywordlocations):
            
            #check if it's the correct keyword
            if self.string[loc+1:loc+1+title_length]==keyword_title:
                
                #extract the string of the keyword
                new_keyword_string=self.string[self.keywordlocations[idx]:self.keywordlocations[idx+1]-1]
                new_keyword_range=[self.keywordlocations[idx],self.keywordlocations[idx+1]-1]
                
                #create keyword object
                new_keyword=Keyword(new_keyword_string,new_keyword_range,self.format)
                keyword_list.append(new_keyword)


        #check if any keywords were found and return list or raise exception
        if len(keyword_list)==0:
            raise Exception(f"No keyword of type *{keyword_title} found")
        else:
            return keyword_list
     
     
                
    #method to replace a keyword in the string with a new keyword object
    def replace_keyword(self,keyword_to_replace:Keyword):
        #define the range and string to be inserted
        insert_range=keyword_to_replace.range
        insert_string=keyword_to_replace.string
        old_keyfile_string=self.string
        
        self.string=old_keyfile_string[0:insert_range[0]] + insert_string 
        + old_keyfile_string[insert_range[1]+1:]
        self.length=len(self.string)
        
    
    
    #method to replace a card in the string with a new card object
    def replace_card(self,card_to_replace:Card):
        #define the range and string to be inserted
        insert_range=card_to_replace.range
        insert_string=card_to_replace.string
        old_keyfile_string=self.string
        
        self.string=old_keyfile_string[0:insert_range[0]] + insert_string 
        + old_keyfile_string[insert_range[1]+1:]
        self.length=len(self.string)
        
    def write_keyfile(self,path:str):
        #check if extension includes .k
        if path[-2:]!=".k":
            path=path + ".k"
        
        #open output file
        with open(path,mode='w') as fout:
            fout.write(self.string)
        
    