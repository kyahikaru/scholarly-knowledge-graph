from neo4j import GraphDatabase


class Neo4jWriter:

    def __init__(self, uri="neo4j://127.0.0.1:7687", user="neo4j", password="neo4j"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def write_graph(self, entities, relations):

        with self.driver.session() as session:

            for entity in entities:
                session.execute_write(self._create_entity, entity)

            for relation in relations:
                session.execute_write(self._create_relation, relation)

    @staticmethod
    def _create_entity(tx, entity):

        query = """
        MERGE (e:Entity {name: $name})
        SET e.type = $type
        """

        tx.run(query, name=entity.name, type=entity.entity_type)

    @staticmethod
    def _create_relation(tx, relation):

        query = """
        MATCH (a:Entity {name: $source})
        MATCH (b:Entity {name: $target})
        MERGE (a)-[r:RELATED_TO {type: $rel_type}]->(b)
        """

        tx.run(
            query,
            source=relation.source,
            target=relation.target,
            rel_type=relation.relation_type,
        )
