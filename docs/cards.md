# Cards

The card object stores the data from a single line of values in a keyword.  This is the fundamental unit from which any parametric edits are performed.

## Attributes

| Attribute | Type | Description|
|---------|-------------|-------------|
| self.string | String | Ascii contents of the keyword |
| self.format | String | Keyword file type, "short" (comma separated), "fixed" (standard PrePost format), or "Long" (double length PrePost format) |
| self.range | list[int] | Start and end character index of the keyword |
| self.comment | Boolean | Denotes whether the card string contains a comment line with the property names. |
| self.length | int | Number of values set by the card. | 
| self.values | list[int, float] | List of all values in the card. |


## Methods

### __init__

Initialize a new Card object

``` python
class Card:
    def __init__(self, input_string: str, input_range: list[int], format: str):

#initialize from KeywordFile
f=KeywordFile("/path/to.k","fixed")
elastic_mat_mods=f.get_keywords("MAT_ELASTIC")
card_one=elastic_mat_mods.get_card(0)

#initialize independently
k=Card("card string here",[0,100],"fixed")
```
__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| input_string | String | Ascii contents of the keyword |
| format | String | Keyword file type, "short" (comma separated), "fixed" (standard PrePost format), or "Long" (double length PrePost format) |
| input_range | list[int] | Start and end character index of the keyword |


__returns__

Keyword object

### __info__

prints debugging information about the card

``` python
def info(self)

f=KeywordFile("/path/to.k","fixed")
elastic_mat_mods=f.get_keywords("MAT_ELASTIC")
card_one=elastic_mat_mods.get_card(0)
card_one.info()

>>Card Format: fixed
>>Card comment included: False
>>Card Range: [16,116]
>>Card Length: 8
>>Card Values: [0, 0, 0, 0, 0, 0, 0, 0]
>>Card String: "0       0       0       0       0       0       0       0"
```

__inputs__

None.

__returns__

Prints the card format, comment status, range, length, values, and string.

### __edit__

Change a value in the card

``` python
def edit(self, edit_index, edit_value):

f=KeywordFile("/path/to.k","fixed")
elastic_mat_mods=f.get_keywords("MAT_ELASTIC")
card_one=elastic_mat_mods.get_card(0)

card_one.edit(0,1)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| edit_index | int | Index of the card value to change |
| edit_value | int or float | New value to insert |


__returns__

Updates card object and corresponding string.
