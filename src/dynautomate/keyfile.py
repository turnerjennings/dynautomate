from .nodes import *
from .card import *
from .keywordclass import Keyword
from .ArrayKeyword import *

# define keyfile object
class KeywordFile:
    def __init__(self, path: str, format: str):
        # define keyword file object from filepath to open

        # read contents of input file
        with open(path) as f:
            keyfile_contents = f.read()
        self.string = keyfile_contents

        # define object properties from inputs
        self.format = format
        self.path = path
        self.length = len(self.string)

        # create an array of the location of every keyword in the file
        indices = []
        index = self.string.find("*")
        while index != -1:
            indices.append(index)
            index = self.string.find("*", index + 1)

        if len(indices) == 0:
            raise Exception("No keywords found in file")

        self.keywordlocations = indices
        self.keywordcount = len(indices)

        # define keyword deck title
        if (
            self.string[self.keywordlocations[1] + 1 : self.keywordlocations[1] + 6]
            == "TITLE"
        ):
            self.title = self.string[
                self.keywordlocations[1] + 7 : self.keywordlocations[2] - 1
            ]
        else:
            self.title = None

    # initialize magic methods
    def __str__(self):
        return f"Keyword file (Title: {self.title} Number of keywords: {self.keywordcount})"

    def __len__(self):
        return self.keywordcount

    # method to print keyfile info
    def info(self):
        print(
            f"Keyword file\nTitle: {self.title}\n"
            + f"File length: {self.length}\n"
            + f"Number of keywords: {self.keywordcount}\n"
            + f"Keyword locations:\n {self.keywordlocations}\n"
        )

    # method to return a list of all keywords of a type in the deck
    def get_keywords(self, keyword_title: str,array=False):
        title_length = len(keyword_title)
        keyword_list = []

        # for each keyword location,
        for idx, loc in enumerate(self.keywordlocations):
            # check if it's the correct keyword
            if self.string[loc + 1 : loc + 1 + title_length] == keyword_title:
                # extract the string of the keyword
                new_keyword_string = self.string[
                    self.keywordlocations[idx] : self.keywordlocations[idx + 1] - 1
                ]
                new_keyword_range = [
                    self.keywordlocations[idx],
                    self.keywordlocations[idx + 1] - 1,
                ]

                # create keyword object

                new_keyword = Keyword(
                    new_keyword_string, new_keyword_range, self.format
                    )

                    
                keyword_list.append(new_keyword)
                
        # check if any keywords were found and return list or raise exception
        if len(keyword_list) == 0:
            raise Exception(f"No keyword of type *{keyword_title} found")
        elif len(keyword_list) == 1:
            return keyword_list[0]
        else:
            return keyword_list


    #method to return an object with all of the nodes in the deck
    def get_nodes(self):
        title_length=4
        
        for idx, loc in enumerate(self.keywordlocations):
            # check if it's the correct keyword
            if self.string[loc + 1 : loc + 1 + title_length] == "NODE":
                new_keyword_string = self.string[
                    self.keywordlocations[idx] : self.keywordlocations[idx + 1] - 1
                ]
                new_keyword_range = [
                    self.keywordlocations[idx],
                    self.keywordlocations[idx + 1] - 1,
                ]

                # create keyword object
                new_keyword = Nodes(
                    new_keyword_string, new_keyword_range, self.format
                )
        
        return new_keyword
        

    def get_elements(self,eltype:str):
        title_length=8+len(eltype)
        keyword_list=[]
        
        for idx, loc in enumerate(self.keywordlocations):
            # check if it's the correct keyword
            if self.string[loc + 1 : loc + 1 + title_length] == "ELEMENT_" + eltype:
                new_keyword_string = self.string[
                    self.keywordlocations[idx] : self.keywordlocations[idx + 1] - 1
                ]
                new_keyword_range = [
                    self.keywordlocations[idx],
                    self.keywordlocations[idx + 1] - 1,
                ]

                # create keyword object
                new_keyword = Elements(
                    new_keyword_string, new_keyword_range, self.format
                )
                keyword_list.append(new_keyword)

        # check if any keywords were found and return list or raise exception
        if len(keyword_list) == 0:
            raise Exception(f"No keyword of type *ELEMENT_{eltype} found")
        elif len(keyword_list) == 1:
            return keyword_list[0]
        else:
            return keyword_list
        
        
        
    # method to replace a keyword in the string with a new keyword object
    def replace_keyword(self, keyword_to_replace):
        # define the range and string to be inserted
        insert_range = keyword_to_replace.range
        insert_string = keyword_to_replace.string
        old_keyfile_string = self.string

        self.string = old_keyfile_string[0 : insert_range[0]] + insert_string
        +old_keyfile_string[insert_range[1] + 1 :]
        self.length = len(self.string)

        # calculate length offsets

    # method to replace a card in the string with a new card object
    def replace_card(self, card_to_replace: Card):
        # define the range and string to be inserted
        insert_range = card_to_replace.range
        insert_string = card_to_replace.string
        old_keyfile_string = self.string

        self.string = old_keyfile_string[0 : insert_range[0]] + insert_string
        +old_keyfile_string[insert_range[1] + 1 :]
        self.length = len(self.string)

    def write_keyfile(self, path: str):
        # check if extension includes .k
        if path[-2:] != ".k":
            path = path + ".k"

        # open output file
        with open(path, mode="w") as fout:
            fout.write(self.string)