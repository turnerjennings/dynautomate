import numpy as np
from .card import *
from .transformation import *

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
        self.title=string_lines[0]


        #check for title
        if string_lines[0].find("TITLE") > -1:
            self.name=string_lines[1]
        else:
            self.name=None
            
        
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

        self.cardcount=len(self.cards)
        
        
        

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

    # method to print the keyword information
    def info(self):
        if len(self.string) > 100:
            string_snippet = self.string[0:500] + "..."
        else:
            string_snippet = self.string

        print(
            "Keyword name: "
            + str(self.name)
            + "\nKeyword format: "
            + str(self.format)
            + "\nKeyword range: "
            + str(self.range)
            + "\nKeyword card count: "
            + str(self.cardcount)
            + "\nKeyword array dimensions:"
            + str(self.array.shape)
            + "\nKeyword cards: \n"
            + str(self.cards)
            + "\nKeyword string: \n"
            + str(string_snippet)
        )
    # method to update the nodes string
    def update_string(self):
        #initialize the new lines with the title
        lines = [self.title]
        if self.name != None:
            lines.append(self.name)
        
        #add cards to lines
        if self.cardcount > 0:
            for i in range(self.cardcount):
                card_to_insert=self.cards[i]
                lines.append(card_to_insert.string)

        #add array to lines
        match self.format:
            case "fixed":
                char_width=10
                for i in range(self.array.shape[0]):
                    line_values=self.array[i, 0:]
                    line_string=""
                    for j in range(self.width):
                        line_string+=f"{int(line_values[j])}".rjust(char_width) 
                    lines.append(line_string)

            case "long":
                char_width=10
                for i in range(self.array.shape[0]):
                    line_values=self.array[i, 0:]
                    line_string=""
                    for j in range(self.width):
                        line_string+=f"{int(line_values[j])}".rjust(char_width) 
                    lines.append(line_string)

            case "short":
                for i in range(self.array.shape[0]):
                    line_values=self.array[i, 0:]
                    line_string=""
                    for j in range(self.width):
                        line_string+=f"{int(line_values[j])}"+","
                    lines.append(line_string)              

        self.string = "\n".join(lines)


class Nodes(ArrayKeyword):
    headercards=0
    width=6

    # method to transform a set of nodes using a transformation operator
    def transform(self, node_set: list[int], operator: Transformation):
        tmatrix = operator.matrix

        for index in node_set:
            # extract nodal coordinates and reformat
            coordinates = self.nodes[index, 1:4]
            coordinates = np.hstack((coordinates, np.array([1])))
            coordinates = coordinates.reshape(-1, 1)

            # apply transformations
            new_coordinates = tmatrix @ coordinates
            print(f"New vector: {new_coordinates}")
            self.nodes[index, 1:4] = new_coordinates[0:3].transpose()
        self.update_string()

    # method to update the nodes string
    def update_string(self):
        lines = ["*NODE"]
        match self.format:
            case "fixed":
                for i in range(self.numnodes):
                    line_values = self.nodes[i, 0:]
                    line_string = (
                        f"{int(line_values[0]):8}".rjust(8)
                        + f"{line_values[1]:11G}".rjust(16)
                        + f"{line_values[2]:11G}".rjust(16)
                        + f"{line_values[3]:11G}".rjust(16)
                        + f"{line_values[4]:8G}".rjust(8)
                        + f"{line_values[5]:8G}".rjust(8)
                    )
                    lines.append(line_string)

            case "long":
                for i in range(self.numnodes):
                    line_values = self.nodes[i, 0:]
                    line_string = (
                        f"{int(line_values[0]):20}".rjust(20)
                        + f"{line_values[1]:15G}".rjust(20)
                        + f"{line_values[2]:15G}".rjust(20)
                        + f"{line_values[3]:15G}".rjust(20)
                        + f"{line_values[4]:15G}".rjust(20)
                        + f"{line_values[5]:15G}"
                    )
                    lines.append(line_string)

            case "short":
                for i in range(self.numnodes):
                    line_values = self.nodes[i, 0:]
                    line_string = (
                        f"{int(line_values[0])}"
                        + ","
                        + f"{line_values[1]}"
                        + ","
                        + f"{line_values[2]}"
                        + ","
                        + f"{line_values[3]}"
                        + ","
                        + f"{line_values[4]}"
                        + ","
                        + f"{line_values[5]}"
                        + ","
                    )
                    lines.append(line_string)

        self.string = "\n".join(lines)

class Elements(ArrayKeyword):
    headercards=0
    width=10

class Set(ArrayKeyword):
    headercards=1
    width=8


                  
        
            


