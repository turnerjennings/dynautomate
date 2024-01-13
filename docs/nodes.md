# Nodes

A special type of the keyword object which stores the nodes of the input deck in a numpy array for efficient modification of points within the field.

## Attributes

| Attribute | Type | Description|
|---------|-------------|-------------|
| self.name | String | Keyword name |
| self.string | String | Ascii contents of the keyword |
| self.format | String | Keyword file type, "short" (comma separated), "fixed" (standard PrePost format), or "Long" (double length PrePost format) |
| self.range | list[int] | Start and end character index of the keyword |
| self.nodes | np.ndarray | Array containing the nodal coordinates |


## Methods

### __init__

Initialize a new Card object

``` python
class Nodes:
    def __init__(self, input_string, input_range, format):

f=KeywordFile("/path/to.k","fixed")
nodal_coords=f.get_nodes()
```
__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| input_string | String | Ascii contents of the keyword |
| format | String | Keyword file type, "short" (comma separated), "fixed" (standard PrePost format), or "Long" (double length PrePost format) |
| input_range | list[int] | Start and end character index of the keyword |


__returns__

Nodes object

### __Transform__

Applies a pre-defined series of transformations to a set of nodes

``` python
def transform(self, node_set, operator):

f=KeywordFile("/path/to.k","fixed")
nodal_coords=f.get_nodes()

node_set=[0,1,2,3,4]

transform_operator=Transformation()
transform_operator.scale(2,0,0)

nodal_coords.transform(node_set,transform_operator)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| node_set | list[int] | indices of each node to apply the transformation to |
| operator | Transformation | Pre-defined transformation operator containing a specified transformation matrix. |

__returns__

Updates the nodal array with new x,y,z coordinates for the node subset.

### __update_string__

Update the contents of self.string to reflect any transformations applied

``` python
def update_string(self):

f=KeywordFile("/path/to.k","fixed")
nodal_coords=f.get_nodes()

node_set=[0,1,2,3,4]

transform_operator=Transformation()
transform_operator.scale(2,0,0)

nodal_coords.transform(node_set,transform_operator)
nodal_coords.update_string()

f.replace_keyword(nodal_coords)
```

__inputs__

None


__returns__

Updates self.string to reflect changes made.