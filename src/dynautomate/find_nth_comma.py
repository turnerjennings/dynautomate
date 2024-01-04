# function to find the nth comma in a comma separated list
# return: int
def find_nth_comma(input_string: str, n: int) -> int:
    position = -1
    for _ in range(n):
        position = input_string.find(",", position + 1)
        if position == -1:
            break  # Break if the nth comma is not found
    return position