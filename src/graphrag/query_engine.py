# src/graphrag/query_engine.py

from neo4j import GraphDatabase
from typing import List


class GraphRAGQueryEngine:

    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self.driver.close()


    def search_entity(self, name: str) -> List[dict]:
        """
        Find entities matching a query string.
        """

        query = """
        MATCH (n)
        WHERE toLower(n.label) CONTAINS toLower($name)
        RETURN n
        LIMIT 10
        """

        with self.driver.session() as session:
            results = session.run(query, name=name)

            return [record["n"] for record in results]


    def get_neighbors(self, entity_id: str) -> List[dict]:
        """
        Retrieve neighboring nodes for an entity.
        """

        query = """
        MATCH (a)-[r]->(b)
        WHERE a.node_id = $entity_id
        RETURN b.label AS neighbor, type(r) AS relation
        LIMIT 20
        """

        with self.driver.session() as session:
            results = session.run(query, entity_id=entity_id)

            return [
                {
                    "neighbor": record["neighbor"],
                    "relation": record["relation"]
                }
                for record in results
            ]


    def query(self, text: str):
        """
        GraphRAG query.
        """

        entities = self.search_entity(text)

        if not entities:
            return {"answer": "No matching entity found."}

        entity = entities[0]

        neighbors = self.get_neighbors(entity["node_id"])

        return {
            "entity": entity["label"],
            "relations": neighbors
        }
