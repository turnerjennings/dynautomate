# Transformation

An object which stores a 3d transformation matrix.  The matrix can be built through applying a sequential series of simple transformations (rotation, translation, scaling).  The resultant compound transformation can then be applied to a node set in the keyword file.

## Attributes

| Attribute | Type | Description|
|---------|-------------|-------------|
| self.matrix | np.ndarray | 4x4 matrix containing the three-dimensional transformation operator |

## Methods

### __init__

Initialize a new Card object

``` python
class Transformation:
    def __init__(self):

transform_operator=Transformation()
```
__inputs__

None.

__returns__

Transformation object containing a 4x4 identity matrix.

### __Scale__

Applies x,y,z scale factors to the transformation operator

``` python
def scale(self, sx, sy, sz):

transform_operator=Transformation()
#scale by 2 in the x-direction
transform_operator.scale(2.0,1.0,1.0)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| sx | float | x-direction scale factor |
| sy | float | y-direction scale factor |
| sz | float | z-direction scale factor |


__returns__

Updates self.matrix with the appropriate scaling operators.

### __Translate__

Applies x,y,z translation to the transformation operator.

``` python
def translate(self, tx, ty, tz):

transform_operator=Transformation()
#shift by 2 in the x-direction
transform_operator.translate(2.0,0,0)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| tx | float | x-direction translation |
| ty | float | y-direction translation |
| tz | float | z-direction translation |


__returns__

Updates self.matrix with the appropriate translation operators.

### __Rotate__

Applies a rotation about an arbitrary axis, defined by two points in xyz space, to the transformation operator.

``` python
def rotate(self, p1, p2, angle):

transform_operator=Transformation()
#rotate by 90 degrees about the x-axis
transform_operator.transform([0,0,0],[1.0,0,0],90)

```

__inputs__

| Attribute | Type | Description|
|---------|-------------|-------------|
| p1 | list[float] | Point 1 for defining rotation axis |
| p2 | list[float] | Point 2 for defining rotation axis |
| angle | float | Angle (in degrees) to rotate the selected nodes about the defined axis |


__returns__

Updates self.matrix with the appropriate rotation operators.