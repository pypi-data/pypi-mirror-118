# rdflib-shim
A compatibility adapter for rdflib version 6.0.

`rdflib_shim` adds a wrapper on the rdflib Graph.serialize method that _always_ has a decode() function, whether the
output is in bytes or as a string

## Usage
```python
from rdflib import Graph, RDF, RDFS
import rdflib_shim

g = Graph()
g.add( (RDFS.Resource, RDF.type, RDFS.resource))
g.serialize(format="turtle")

```
