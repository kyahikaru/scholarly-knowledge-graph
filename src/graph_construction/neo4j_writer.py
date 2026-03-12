from neo4j import GraphDatabase


class Neo4jWriter:

    def __init__(self, uri="neo4j://127.0.0.1:7687", user="neo4j", password="NEO4J_PASSWORD"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def write_graph(self, entities, relations):

        # Build ID → name lookup
        entity_lookup = {e.entity_id: e.canonical_name for e in entities}

        with self.driver.session() as session:

            for entity in entities:
                session.execute_write(self._create_entity, entity)

            for relation in relations:
                session.execute_write(self._create_relation, relation, entity_lookup)

    @staticmethod
    def _create_entity(tx, entity):

        query = """
        MERGE (e:Entity {name: $name})
        SET e.type = $type
        """

        entity_name = getattr(entity, "canonical_name", None)

        if not entity_name:
            return

        entity_name = str(entity_name).strip().lower()
        entity_type = getattr(entity, "entity_type", "ENTITY")

        tx.run(query, name=entity_name, type=entity_type)

    @staticmethod
    def _create_relation(tx, relation, entity_lookup):

        source = entity_lookup.get(relation.source_entity_id)
        target = entity_lookup.get(relation.target_entity_id)

        if not source or not target:
            return

        query = """
        MATCH (a:Entity {name: $source})
        MATCH (b:Entity {name: $target})
        MERGE (a)-[:USED_ON]->(b)
        """

        tx.run(query, source=source, target=target)
