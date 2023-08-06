from rdflib import Graph


class DecodableStr(str):
    """ A string with a decode method """
    def decode(self) -> str:
        return self

orig_serialize = Graph.serialize
def serialize_shim(*args, **kwargs) -> DecodableStr:
    rval = orig_serialize(*args, **kwargs)
    return DecodableStr(rval) if isinstance(rval, str) else rval

Graph.serialize = serialize_shim
