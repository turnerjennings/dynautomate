# Keyfile

The keyfile object contains and manages the contents of the entire LS-DYNA solver deck.  Methods for this object are used to extract subsets of interest for iteration, to replace values in the keyword deck, and to write subsequent iterations of the original file.

## Attributes


## Methods

### __init__

Initialize a new keyword file object from a file input

``` python
class KeywordFile:
    def __init__(self, path, format):


f=KeywordFile("/path/to.k","fixed")

```
__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| path | String | Path to keyword file |
| format | String | Keyword file type, "short" (comma separated), "fixed" (standard PrePost format), or "Long" (double length PrePost format)|

__returns__

KeywordFile object

### __info__

prints debugging information about the keyword file

``` python
def info(self)

f=KeywordFile("/path/to.k","fixed")
f.info()

>>Keyword file
>>Title: LS-DYNA Keyword Input
>>File length: 1000
>>Number of keywords: 4
>>Keyword locations: [10,52,100,516]

```

__inputs__

None.

__returns__

Prints the keyword file name (*TITLE keyword), file length (# characters), number of individual keywords, and the location of the starting character of each keyword.

### __get_keywords__

Retrieve all keywords of a specified type

``` python
def get_keywords(self, keyword_title):

f=KeywordFile("/path/to.k","short")

elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| keyword_title | String | keyword to search for, optional to include the "*" keyword delimeter |


__returns__

Returns Keyword object (one matching keyword found) or list of Keyword objects (multiple matching keywords found)

### get_nodes

Create a Nodes object with all nodes in the keyword file

``` python
def get_nodes(self):

f=KeywordFile("/path/to.k","short")

f_nodes=f.get_nodes()

```

__inputs__

None.

__returns__

Returns a Nodes object (special keyword type) with the node numbers and coordinates stored in numpy array format.

### replace_keyword

Replace an existing keyword in the solver deck with a new one.

``` python
def replace_keyword(self, keyword_to_replace):

f=KeywordFile("/path/to.k","short")

elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

new_mat_mod=elastic_mat_mods[0].edit_card(0,0,1)

f.replace_keyword(new_mat_mod)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| keyword_to_replace | Keyword object | Updated keyword containing the replacement context information |


__returns__

Updates the KeywordFile object string and keywordlocation information.

### replace_card
Replace an existing card in the solver deck with a new one.

``` python
def replace_keyword(self, card_to_replace):

f=KeywordFile("/path/to.k","short")

elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

new_mat_card_one=elastic_mat_mods[0].get_card

new_mat_card_one.edit(0,0,1)

f.replace_card(new_mat_card_one)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| card_to_replace | Card object | Updated Card containing the replacement context information |


__returns__

Updates the KeywordFile object string and keywordlocation information.


### write_keyfile
Writes a new keyword file output to the specified directory.

``` python
def write_keyfile(self, path):

f=KeywordFile("/path/to.k","short")

elastic_mat_mods=f.get_keywords("MAT_ELASTIC")

new_mat_mod=elastic_mat_mods[0].edit_card(0,0,1)

f.replace_keyword(new_mat_mod)

f.write_keyfile("/path/to_new.k")

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| path | String | File path to preferred output location |


__returns__

New .k file in specified directory.
