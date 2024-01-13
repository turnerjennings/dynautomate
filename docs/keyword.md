# Keyword

The keyword object contains the data of a single keyword.  This includes all of the card objects associated with the keyword and its location in the corresponding solver deck.

## Attributes

| Attribute | Type | Description|
|---------|-------------|-------------|
| self.name | String | Keyword name |
| self.string | String | Ascii contents of the keyword |
| self.format | String | Keyword file type, "short" (comma separated), "fixed" (standard PrePost format), or "Long" (double length PrePost format) |
| self.range | list[int] | Start and end character index of the keyword |
| self.cardcount | int | Number of cards in the keyword |
| self.cards | list[Card] | list containing each card in the keyword |





## Methods

### __init__

Initialize a new keyword object

``` python
class Keyword:
    def __init__(self, input_string, input_range, format):

#initialize from KeywordFile
f=KeywordFile("/path/to.k","fixed")
elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

#initialize independently
k=Keyword("keyword string here",[0,100],"fixed")
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

prints debugging information about the keyword

``` python
def info(self)

f=KeywordFile("/path/to.k","fixed")
elastic_mat_mods=f.get_keywords("MAT_ELASTIC")
elastic_mat_mods.info()

>>Keyword name: MAT_ELASTIC
>>Keyword format: fixed
>>Keyword range: [512,612]
>>Keyword card count: 1
>>Keyword cards: [...]
>>Keyword string: "*MAT_ELASTIC\n..."
```

__inputs__

None.

__returns__

Prints the keyword name, keyword format, range, card count, cards, and keyword string.

### __get_card__

Retrieve a specified card from the keyword

``` python
def get_card(self, card_num):

f=KeywordFile("/path/to.k","short")

elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

elastic_mat_mods_one=elastic_mat_mods.get_card(0)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| card_num | int | Index of the card to return |


__returns__

Returns Card object.

### __replace_card__

Replaces a selected card in the keyword with a new card object

``` python
def replace_card(self, card_num, card_replace):

f=KeywordFile("/path/to.k","short")

elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

new_card=Card("1,0,0,0,0",[10,22],"short")

elastic_mat_mods.replace_card(0,new_card)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| card_num | int | Index of the card to return |
| card_replace | Card | New card to insert | 

__returns__

Updates the selected keyword to include a new card.

