# Dynautomate

A workflow for building parametric DOEs in LS-DYNA on HPC 

# Objects
## keyfile

### Attributes

*name:* (String) title of keyword file
*format:* (String) keyword syntax format, either comma separated ("short"), standard("fixed"), or long format ("long")
*path:* (String) path to keyword file
*keywordcount:* (Int) Number of unique keywords in the file
*keywordlocations:* (List[int]) list of the location of the start of each keyword
*length:* (Int) number of characters in the keyword file
*string:* (String) text contents of the keyword file

### Methods
```python
def __init__(self, path: str, format: str) -> KeywordFile:
```

Open and parse a keyword file.

**Arguments**

*path:* (String) path to keyword file
*format:* (String) keyword format; "short", "fixed", or "long"



```python
def info(self) -> str:
```

Print keyfile summary



```python
def get_keywords(self, keyword_title: str) -> list[Keyword]:
```

Retrieve all instances of a keyword with a given name in the keyfile

**Arguments**

*keyword_title:* (String) name of the keyword to search for



```python
def get_nodes(self) -> Nodes:
```

Retrieves the *NODE keyword as a Nodes object

```python
def replace_keyword(self, keyword_to_replace: Keyword | Nodes):
```

Replace an existing keyword with a different keyword of the same type

**Arguments**

*keyword_to_replace:* (Keyword or Nodes) object to replace current object in the string





## Examples
### Edit properties of a keyword
```python
#import a fixed-width keyword file
keyword_file=keyfile.KeywordFile("example_keyword.k","fixed")

#extract all copies the desired keyword
mat_keywords=keyword_file.get_keywords("MAT_ELASTIC")

#define the keyword to be modified
keyword_to_modify=mat_keywords[0]

#edit the second value in the first card
keyword_to_modify.edit_card(0,1,1e10)

#insert into keyfile deck
keyword_file.replace_keyword(keyword_to_modify)

#write out new keyfile deck
keyword_file.write_keyfile("new_keyword.k")
```

### Create parametric copies of a keyword
```python
#import a comma-separated keyword file
keyword_file=keyfile.KeywordFile("example_keyword.k","short")

#extract all copies the desired keyword
mat_keywords=keyword_file.get_keywords("MAT_ELASTIC")

#define the keyword to be modified
keyword_to_modify=mat_keywords[0]

#define the card to be modified
card_to_modify=keyword_to_modify.get_card(0)

#create parametric simulation definitions
new_values=[1e10,2e10,3e10]
new_names=["low.k","medium.k","high.k"]

#create parametric simulation copies
for i in range(3):
    new_card=card_to_modify.edit(1,new_values[i])
    keyword_file.replace_card(new_card)
    keyword_file.write_keyfile(new_names[i])
```

### Create a transformation operator
```python
transform_operator=keyfile.Transformation()

#add translation by 2 in x direction
transform_operator.translate(2,0,0)

#add scale y by 5
transform_operator.scale(0,5,0)

#rotate by 90 degrees about arbitrary axis
transform_operator.rotate([0,0,0],[1,5,6],90)
```

### Apply a transformation to a node set
```python
#import a long format keyword file
keyword_file=keyfile.KeywordFile("example_keyword.k","long")

#retrieve nodes
keyfile_nodes=keyword_file.get_nodes()

#define transformation
transform_operator=keyfile.Transformation()
transform_operator.rotate([0,0,0],[1,5,6],90)

#define node set to be transformed
node_set=[0,1,2,3,100]

#apply transformation to nodes
keyfile_nodes.transform(node_set,transform_operator)

#write to keyfile and write output
keyword_file.replace_keyword(keyfile_nodes)
keyword_file.write_keyfile("new_keyword.k")
```
