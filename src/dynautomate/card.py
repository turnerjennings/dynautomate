from is_float import *
from find_nth_comma import *
# define card object
class Card:
    def __init__(self, input_string: str, input_range: list[int], format: str):
        self.string = input_string
        self.format = format
        self.range = input_range

        # extract length and values
        match self.format:
            case "fixed":  # if the card is space delimitted
                card_lines = input_string.split("\n")

                # check if there is a comment line or not
                if card_lines[0][0:1] == "$":
                    self.comment = True
                    card_length = len(card_lines[0])
                    card_lines[1].ljust(card_length)
                    card_lines.pop(0)

                else:
                    self.comment = False
                    card_length = len(card_lines[0])

                card_values = [
                    card_lines[0][i : i + 10] for i in range(0, card_length, 10)
                ]

                self.length = len(card_values)

                # convert values to int or float
                for i, val in enumerate(card_values):
                    value = val.lstrip()
                    if value.isdigit() == True:
                        card_values[i] = int(value)

                    elif is_float(value) == True:
                        card_values[i] = float(value)

                    elif value == "":
                        card_values[i] = "          "

                    else:
                        raise ValueError(
                            "Error parsing fixed card format: Card value at position "
                            + str(i)
                            + " is not an integer or a float"
                        )

                self.values = card_values

            case "short":
                card_lines = input_string.split("\n")

                # check if there is a comment line or not
                if card_lines[0][0:1] == "$":
                    self.comment = True
                    card_lines.pop(0)
                else:
                    self.comment = False

                card_values = card_lines[0].split(",")

                self.length = len(card_values)

                # convert values to int or float
                for i, value in enumerate(card_values):
                    if value.isdigit() == True:
                        card_values[i] = int(value)

                    elif is_float(value) == True:
                        card_values[i] = float(value)

                    elif value == "" or value.isspace() == True:
                        card_values[i] = ""
                    else:
                        raise ValueError(
                            "Error parsing short card format: Card value at position "
                            + str(i)
                            + " is not an integer or a float"
                        )

                self.values = card_values

            # case for if the input isn't a fixed or a short
            case _:
                raise ValueError("Card format unexpected or unsupported")

    # define object magic methods
    def __str__(self):
        return f"Card(Number of values: {self.length}, Range: {self.range})"

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.edit(key, value)

    # method to print card info
    def info(self):
        print(
            "Card Format: "
            + str(self.format)
            + "\nCard comment included: "
            + str(self.comment)
            + "\nCard Range: "
            + str(self.range)
            + "\nCard Length: "
            + str(self.length)
            + "\nCard Values: "
            + str(self.values)
            + "\nCard String: \n"
            + str(self.string)
        )

    def edit(self, edit_index: int, edit_value):
        # check inputs
        if edit_index > self.length or edit_index < 0:
            raise IndexError("Value index out of range")

        # check write format
        match self.format:
            case "fixed":
                # check if the value being inserted is the same as the existing value
                if (
                    type(self.values[edit_index]) == type(edit_value)
                    or self.values[edit_index] == 0
                    or self.values[edit_index] == "          "
                ):
                    # check if card has comment and adjust start location accordingly
                    if self.comment == True:
                        preceding_value_end = (
                            self.string.find("\n") + 10 * edit_index + 1
                        )

                    elif self.comment == False:
                        preceding_value_end = 10 * edit_index

                    # find the end of the new value in the array
                    edit_value_end = preceding_value_end + 10

                    # define the edit range and the value to be replaced
                    value_to_replace = self.string[preceding_value_end:edit_value_end]
                    edit_range = edit_value_end - preceding_value_end

                    # edit the value in the array
                    self.values[edit_index] = edit_value

                    # check if value is integer or float, write accordingly
                    if type(edit_value) == float:
                        new_string = (
                            self.string[0:preceding_value_end]
                            + f"{edit_value:#.{edit_range-5}G}".rjust(10)
                            + self.string[edit_value_end:]
                        )
                        self.string = new_string

                    elif type(self.values[edit_index]) == int:
                        new_string = (
                            self.string[0:preceding_value_end]
                            + f"{edit_value:{edit_range}}"
                            + self.string[edit_value_end:]
                        )
                        self.string = new_string

                    else:
                        raise ValueError(
                            "The value inserted in the keyword is not an int or a float"
                        )

                else:
                    raise TypeError(
                        "Input value type does not match existing data type"
                    )

            case "short":
                # check if the value being inserted is the same as the existing value
                if (
                    type(self.values[edit_index]) == type(edit_value)
                    or self.values[edit_index] == 0
                    or self.values[edit_index] == ""
                ):
                    # check if card has comment and adjust start location accordingly
                    comma_location = find_nth_comma(self.string, edit_index)

                    # if there is no commas on the line to start
                    if comma_location < 0:
                        preceding_value_end = 0
                        edit_value_end = 1
                    else:
                        preceding_value_end = comma_location
                        edit_value_end = self.string.find(",", preceding_value_end + 1)

                    # find the end of the new value in the array

                    # define the edit range and the value to be replaced
                    value_to_replace = self.string[preceding_value_end:edit_value_end]

                    # edit the value in the array
                    self.values[edit_index] = edit_value

                    # check if value is integer or float, write accordingly
                    if type(edit_value) == float:
                        if comma_location < 0:
                            new_string = (
                                self.string[0 : preceding_value_end + 1]
                                + f"{edit_value:#.5G}"
                                + ","
                                + self.string[edit_value_end:]
                            )
                        else:
                            new_string = (
                                self.string[0 : preceding_value_end + 1]
                                + f"{edit_value:#.5G}"
                                + self.string[edit_value_end:]
                            )
                        self.string = new_string

                    elif type(self.values[edit_index]) == int:
                        if comma_location < 0:
                            new_string = (
                                self.string[0 : preceding_value_end + 1]
                                + str(edit_value)
                                + ","
                                + self.string[edit_value_end:]
                            )
                        else:
                            new_string = (
                                self.string[0 : preceding_value_end + 1]
                                + str(edit_value)
                                + self.string[edit_value_end:]
                            )
                        self.string = new_string

                    else:
                        raise ValueError(
                            "The value inserted in the keyword is not an int or a float"
                        )
                    print(
                        "New Values: "
                        + str(self.values)
                        + "\nNew string: \n"
                        + str(self.string)
                    )

                else:
                    raise TypeError(
                        "Input value type does not match existing data type"
                    )

            case "long":
                # check if the value being inserted is the same as the existing value
                if (
                    type(self.values[edit_index]) == type(edit_value)
                    or self.values[edit_index] == 0
                ):
                    # check if card has comment and adjust start location accordingly
                    if self.comment == True:
                        preceding_value_end = (
                            self.string.find("\n") + 20 * edit_index + 1
                        )

                    elif self.comment == False:
                        preceding_value_end = 20 * edit_index + 1

                    # find the end of the new value in the array
                    edit_value_end = preceding_value_end + 20

                    # define the edit range and the value to be replaced
                    value_to_replace = self.string[preceding_value_end:edit_value_end]
                    edit_range = edit_value_end - preceding_value_end

                    print(
                        "Range: "
                        + str([preceding_value_end, edit_value_end])
                        + "\nStart character: "
                        + self.string[preceding_value_end]
                        + "\nEnd character: "
                        + self.string[edit_value_end]
                        + "\nFull string to be replaced: {"
                        + str(value_to_replace)
                        + "}"
                    )

                    # edit the value in the array
                    self.values[edit_index] = edit_value

                    # check if value is integer or float, write accordingly
                    if type(edit_value) == float:
                        new_string = (
                            self.string[0:preceding_value_end]
                            + f"{edit_value:#.{edit_range-5}G}".rjust(20)
                            + self.string[edit_value_end:]
                        )
                        self.string = new_string

                    elif type(self.values[edit_index]) == int:
                        new_string = (
                            self.string[0:preceding_value_end]
                            + f"{edit_value:{edit_range}}"
                            + self.string[edit_value_end:]
                        )
                        self.string = new_string

                    else:
                        raise ValueError(
                            "The value inserted in the keyword is not an int or a float"
                        )
                    print(
                        "New Values: "
                        + str(self.values)
                        + "\nNew string: \n"
                        + str(self.string)
                    )

                else:
                    raise TypeError(
                        "Input value type does not match existing data type"
                    )

            case _:
                raise ValueError("Unknown card format")