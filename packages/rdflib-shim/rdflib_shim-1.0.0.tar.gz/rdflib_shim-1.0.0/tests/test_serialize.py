import unittest

from rdflib import Graph, RDF, RDFS


class SerializeTestCase(unittest.TestCase):
    def test_as_str(self):
        g = Graph()
        g.add( (RDFS.Resource, RDF.type, RDFS.Resource))
        with self.assertRaises(AttributeError) as e:
            g.serialize(format="turtle").decode()
        self.assertIn("object has no attribute 'decode'", str(e.exception))
        import rdflib_shim
        self.assertEqual('''@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

rdfs:Resource a rdfs:Resource .''', g.serialize(format="turtle").decode().strip())


if __name__ == '__main__':
    unittest.main()
