import numpy as np
from .card import *

class ArrayKeyword:

    headercards=0
    width=10
    
    def __init__(self, input_string: str, input_range: list[int], format:str):
        
        #define attributes from input block
        self.string = input_string
        self.format = format
        self.range = input_range
        self.cards = []
        string_lines=self.string.splitlines()


        #check for title
        if string_lines[0].find("TITLE") > -1:
            self.name=string_lines[0] + ": " + string_lines[1]
        else:
            self.name=string_lines[0]
            
        
        if self.headercards > 0:
            range_count = 0
            card_count = 0
            comment_line = None
            for i, line in enumerate(string_lines):
                # check if the line is a comment, if so store it
                if line.find("$") >= 0:
                    comment_line = line

                # if the line is not a comment and not the start of a new keyword
                elif line.find("*") < 0:
                    # check if the previous line was a comment
                    if comment_line != None:
                        # if yes, add previous comment line to current comment line
                        card_string = comment_line + "\n" + line
                        comment_line = None

                    else:
                        # if no, set card string to current line
                        card_string = line

                    # create a new card using the current line and append it to the array
                    new_card = Card(
                        card_string, [range_count, range_count + len(line)], self.format
                    )
                    self.cards.append(new_card)

                    # update the start point of the next range
                    range_count += len(card_string) + 1

                    #update card count
                    card_count += 1

                    #check if number of header cards has been satisfied
                    if card_count == self.headercards:
                        break
                else:
                    range_count += len(line) + 1
            array_start=i+1
            self.arrayrange=[range_count, self.range[1]]
        else:
            array_start=1 
            self.arrayrange=[self.range[0] + len(string_lines[0]) + 1, self.range[1]]
        
        
        

        array_string=string_lines[array_start:]

        numlines = len(array_string)
        self.array = np.empty((numlines, self.width))

        # split nodal values depending on format
        for idx, string in enumerate(array_string):
            match self.format:
                case "fixed":
                    line_values = string.split()
                    self.array[idx, :] = line_values

                case "long":
                    line_values = string.split()
                    self.array[idx, :] = line_values

                case "short":
                    line_values = string.split(",")
                    self.array[idx, :] = line_values

class Nodes(ArrayKeyword):
    headercards=0
    width=6

class Elements(ArrayKeyword):
    headercards=0
    width=10

class Set(ArrayKeyword):
    headercards=1
    width=8


                  
        
            


