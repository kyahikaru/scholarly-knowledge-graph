from neo4j import GraphDatabase


class Neo4jWriter:

    def __init__(self, uri="neo4j://127.0.0.1:7687", user="neo4j", password="NEO4J_PASSWORD"):
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

        # Use canonical entity name instead of object serialization
        entity_name = getattr(entity, "canonical_name", None)

        if not entity_name:
            return

        entity_name = str(entity_name).strip().lower()
        entity_type = getattr(entity, "entity_type", "ENTITY")

        tx.run(
            query,
            name=entity_name,
            type=entity_type
        )

    @staticmethod
    def _create_relation(tx, relation):

        source = getattr(relation, "source_text", getattr(relation, "source", None))
        target = getattr(relation, "target_text", getattr(relation, "target", None))

        # Clean values
        source = str(source).strip().lower() if source else None
        target = str(target).strip().lower() if target else None

        # Skip invalid relations
        if not source or not target:
            return

        if source == "unknown" or target == "unknown":
            return

        query = """
        MERGE (a:Entity {name: $source})
        MERGE (b:Entity {name: $target})
        MERGE (a)-[:RELATED_TO]->(b)
        """

        tx.run(
            query,
            source=source,
            target=target
        )
