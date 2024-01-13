# Dynautomate

Workflows for parametric DOE for LS-DYNA on HPC.  This package is still a work in progress.

## Installation

Package is not available on pip pending full testing.  Repository can be downloaded and installed locally:

    py -m pip install .


## Project Overview

The objective of this python package is to provide a set of tools for building workflows to set up parametric LS-DYNA simulations in an HPC environment.  The object structure of the package follows the same structure as the LS-DYNA keyword input files:

```
keyfile
|-keyword 1
| |-card 1
| |-card 2
| |-card 3
|-keyword 2
| |-card 1
| |-card 2
|-etc...
```

### Parameter editing

An initial keyword file is loaded in.  Subsequently, individual keywords and cards can be located and edited or replaced to create new parametric copies of the simulation:

``` python

import dynautomate as dyna

#load the keyword file
file=dyna.KeywordFile("/path/to.k","fixed")

#create a keyword object
t_term=file.get_keywords("CONTROL_TERMINATION")

#edit a card in the keyword object
t_term.edit_card(0,0,0.01)

#insert updated keyword into the keyword file
f.replace_keyword(t_term)

#write new keyword file
f.write_keyfile("/path/to_new.k")

```

### Mesh editing

In addition to editing properties, basic parametric mesh changes can be performed using transformations:

``` python
import dynautomate as dyna

#initialize empty transformation operator
transform_operator=keyfile.Transformation()

#add translation by 2 in x direction
transform_operator.translate(2,0,0)

#add scale y by 5
transform_operator.scale(0,5,0)

#rotate by 90 degrees about arbitrary axis
transform_operator.rotate([0,0,0],[1,5,6],90)

#import a long format keyword file
keyword_file=keyfile.KeywordFile("example_keyword.k","long")

#retrieve nodes
keyfile_nodes=keyword_file.get_nodes()

#define node set to be transformed
node_set=[0,1,2,3,100]

#apply transformation to nodes
keyfile_nodes.transform(node_set,transform_operator)

#write to keyfile and write output
keyword_file.replace_keyword(keyfile_nodes)
keyword_file.write_keyfile("new_keyword.k")

```

For details on the full features of each object type, refer to each object documentation page at the top