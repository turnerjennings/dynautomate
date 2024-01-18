from .card import *

# define keyword object
class Keyword:
    def __init__(self, input_string: str, input_range: list[int], format: str):
        # initialize basic properties
        self.string = input_string
        self.format = format
        self.range = input_range
        self.cards = []

        # check if the string contains comments and the title block
        end_first_line = input_string.find("\n")
        self.name = input_string[0:end_first_line]

        # for each line in the self, sort according to title, comment, and values
        range_count = 0
        comment_line = None
        for i, line in enumerate(input_string.splitlines()):
            # check if the line is a comment, if so store it
            if line.find("$") >= 0:
                comment_line = line

            # if the line is not a comment
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
            else:
                range_count += len(line) + 1

        # count the number of cards
        self.cardcount = len(self.cards)

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
            + "\nKeyword cards: \n"
            + str(self.cards)
            + "\nKeyword string: \n"
            + str(string_snippet)
        )

    # define magic methods
    def __str__(self):
        return f"Keyword(Number of cards: {self.cardcount}, Range: {self.range})"

    def __len__(self):
        return self.cardcount

    def __getitem__(self, key):
        return self.cards[key]

    def __setitem__(self, key, value):
        self.edit_card(key, value)

    # method to retrieve a card from the list as a new object outside of the keyword
    def get_card(self, card_num: int):
        return self.cards[card_num]

    # method to edit a card without retrieving it
    def edit_card(self, card_num, edit_index: int, edit_value):
        # edit the card object
        self.cards[card_num].edit(edit_index, edit_value)

        # define the string to be inserted into the keyword string
        new_card_string = str(self.cards[card_num].string)

        # define the range of indices to be replaced
        insert_range = self.cards[card_num].range

        # insert the values into the string
        new_keyword_string = (
            self.string[: insert_range[0]]
            + new_card_string
            + self.string[insert_range[1] :]
        )
        self.string = new_keyword_string

    # method to replace a card with a new card
    def replace_card(self, card_num, card_replace):
        self.cards[card_num] = card_replace

        # define the string to be inserted into the keyword string
        new_card_string = str(self.cards[card_num].string)

        # define the range of indices to be replaced
        insert_range = self.cards[card_num].range

        # insert the values into the string
        new_keyword_string = (
            self.string[: insert_range[0]]
            + new_card_string
            + self.string[insert_range[1] :]
        )
        self.string = new_keyword_string