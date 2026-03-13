from neo4j import GraphDatabase


class GraphRAG:

    def __init__(self, uri, user, password):

        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def query(self, cypher):

        with self.driver.session() as session:

            result = session.run(cypher)

            return [r.data() for r in result]
