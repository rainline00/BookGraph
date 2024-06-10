from pathlib import Path
from nicegui import ui, app
from bookgraph.mermaid import draw_graph
from bookgraph.loader import MermaidGraphGenerator

PROJECT_ROOT = Path(__file__).parent.parent
BOARD_DIR = PROJECT_ROOT / "data" / "board"

generator = MermaidGraphGenerator(hash_with_move_number=True)
# draw_graph(book_graph)

app.add_static_files("/board", BOARD_DIR)
edges = "\n".join(
    [
        f"{edge[1]}[{edge[1]}] --> {edge[2]}[{edge[2]}]"
        for edge in generator.edge_df.itertuples()
    ]
)
graph = f"""graph
{edges}
"""
with open("./tmp", mode="w") as f:
    print(graph, file=f)
ui.mermaid(graph)
data = {"value": 0}
ui.number(
    label="Number",
    value=0,
    on_change=lambda e: ui.mermaid(
        generator.generate_mermaid_graph(indent=0, board_from=e.value)
    ),
)
ui.run()
