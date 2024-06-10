from neo4j import GraphDatabase
from pathlib import Path
from bookgraph.reader import YaneuraBookReader
# Define correct URI and AUTH arguments (no AUTH by default)

URI = "bolt://localhost:7687"
AUTH = ("", "")
PROJECT_ROOT = Path(__file__).parent.parent.parent
BOOK_DB_PATH = PROJECT_ROOT / "data" / "book.db"

query = "MERGE (b_from:Board{sfen: $sfen_from})-[r:MOVE_TO{chosen_move: $chosen_move, expected_move:$expected_move, evaluation_value: $evaluation_value, depth: $depth}]->(b_to:Board{sfen: $sfen_to}) RETURN r"
with GraphDatabase.driver(URI, auth=AUTH) as client:
    # Check the connection
    client.verify_connectivity()
    reader = YaneuraBookReader(hash_with_move_number=True)
    for node in reader.from_file(BOOK_DB_PATH):
        candidate_moves = node.candidate_moves
        for move in candidate_moves:
            records, summary, keys = client.execute_query(
                query,
                sfen_from=move.sfen,
                chosen_move=move.chosen_move_code,
                expected_move=move.expected_next_move_code,
                evaluation_value=move.evaluation_value,
                depth=move.metadata["0"],
                sfen_to=move.next_sfen,
                database_="memgraph",
            )
