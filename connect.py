from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

with open("data.json", "r") as f:
    data = json.load(f)

source_domain = data["metadata"]["source_domain"]
extracted_at = data["metadata"]["extracted_at"]

with driver.session() as session:

    for triple in data["triples"]:

        subject = triple["subject"]
        predicate = triple["predicate"]
        obj = triple["object"]
        source_url = triple["source_url"]
        is_contested = triple["is_contested"]

        query = f"""
        MERGE (s:Entity {{name: $subject}})
        MERGE (o:Entity {{name: $object}})
        MERGE (s)-[r:{predicate}]->(o)

        SET r.source_url = $source_url
        SET r.is_contested = $is_contested
        SET r.source_domain = $source_domain
        SET r.extracted_at = $extracted_at
        """

        session.run(
            query,
            subject=subject,
            object=obj,
            source_url=source_url,
            is_contested=is_contested,
            source_domain=source_domain,
            extracted_at=extracted_at
        )

driver.close()

print("Graph imported successfully!")
