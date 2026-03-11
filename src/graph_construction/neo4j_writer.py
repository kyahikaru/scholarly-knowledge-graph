from neo4j import GraphDatabase


class Neo4jWriter:

    def __init__(self, uri="neo4j://127.0.0.1:7687", user="neo4j", password="12345678"):
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

        entity_name = str(entity)
        entity_type = getattr(entity, "entity_type", "ENTITY")

        tx.run(
            query,
            name=entity_name,
            type=entity_type
        )

    @staticmethod
    def _create_relation(tx, relation):

        query = """
        MERGE (a:Entity {name: $source})
        MERGE (b:Entity {name: $target})
        MERGE (a)-[:RELATED_TO]->(b)
        """

        source = str(getattr(relation, "source_text", getattr(relation, "source", "unknown")))
        target = str(getattr(relation, "target_text", getattr(relation, "target", "unknown")))

        tx.run(
            query,
            source=source,
            target=target
        )
