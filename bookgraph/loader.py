from pathlib import Path
import pandas as pd
from bookgraph.reader import YaneuraBookReader
from cshogi import Board

PROJECT_ROOT = Path(__file__).parent.parent
BOARD_DIR = PROJECT_ROOT / "data" / "board"
DB_PATH = PROJECT_ROOT / Path("data/book.db")


class MermaidGraphGenerator:
    def __init__(
        self,
        db_path: Path = DB_PATH,
        board_dir: Path = BOARD_DIR,
        offset: int | None = 300,
        hash_with_move_number: bool = False,
    ):
        self.reader = YaneuraBookReader(hash_with_move_number=hash_with_move_number)
        self.db_path = db_path
        self.board_dir = board_dir
        self.nodes = list(self.reader.from_file(db_path))
        self.hash_with_move_number = hash_with_move_number
        if offset:
            self.nodes = self.nodes[:offset]

        df = pd.DataFrame(self.nodes, columns=["node"])
        df["board"] = df["node"].map(lambda x: x.sfen_for_hash)
        df["next_move"] = df["node"].map(
            lambda x: x.candidate_moves[0].chosen_move_code
        )
        df["move_number"] = df["node"].map(lambda x: x.board.move_number)

        self.moves = []
        for moves_list in (node.candidate_moves for node in self.nodes):
            self.moves += moves_list
        board_set = set(move.sfen_for_hash for move in self.moves) | set(
            move.next_sfen_for_hash for move in self.moves
        )
        self.sfen_to_id_dict = {
            sfen_for_hash: idx for idx, sfen_for_hash in enumerate(board_set)
        }
        df_move = pd.DataFrame(self.moves, columns=["move"])
        df_move["from"] = df_move["move"].map(
            lambda x: self.sfen_to_id_dict[x.sfen_for_hash]
        )
        df_move["to"] = df_move["move"].map(
            lambda x: self.sfen_to_id_dict[x.next_sfen_for_hash]
        )
        self.edge_df = df_move[["from", "to"]].copy()
        self.node_df = pd.DataFrame(
            self.sfen_to_id_dict.keys(),
            columns=["title"],
            index=self.sfen_to_id_dict.values(),
        )
        self.node_df["id"] = self.node_df.index
        self.node_df["board"] = self.node_df["title"].map(lambda x: Board(sfen=x))
        self.node_df["move_number"] = self.node_df["board"].map(lambda x: x.move_number)
        self.save_boards_svg()

    def save_boards_svg(self):
        for node in self.node_df.itertuples(index=True):
            with open(self.board_dir / f"board_{node[0]}.svg", mode="w") as f:
                f.write(str(node.board.to_svg()))

    def generate_mermaid_graph(self, indent: int = 1, board_from: int | None = 0):
        if board_from is not None:
            while sum(self.edge_df["from"] == board_from) == 0:
                print(
                    f"board_{board_from} do not have child node. try board_{board_from+1}"
                )
                board_from += 1
        connected_node = set([board_from]) if board_from is not None else set()
        if self.hash_with_move_number:
            groupby = self.node_df.groupby("move_number")
            move_numbers = sorted(list(groupby.groups.keys()))
            nodes = ""
            current_boards = [board_from] if board_from is not None else []
            for i, move_number in enumerate(move_numbers):
                if board_from is not None:
                    for current_board in current_boards:
                        connected_node |= set(
                            self.edge_df[self.edge_df["from"] == int(current_board)][
                                "to"
                            ]
                        )
                    current_boards = [
                        id
                        for id in groupby.get_group(move_number)["id"]
                        if id in connected_node
                    ]
                    print(current_boards, connected_node)
                    if current_boards:
                        nodes += f"{'\t' * indent}subgraph turn_{move_number}[{move_number}手目]\n"
                        nodes += (
                            "\n".join(
                                [
                                    f"{'\t' * indent}board_{idx}(<img src='/board/board_{idx}.svg' width='69' height='59.4' /><br>局面{idx})"
                                    for idx in current_boards
                                ]
                            )
                            + f"\n{'\t' * indent}end\n"
                        )
                else:
                    current_board = groupby.get_group(move_number)["id"]
                    if current_boards:
                        nodes += f"{'\t' * indent}subgraph turn_{move_number}[{move_number}手目]\n"
                        nodes += (
                            "\n".join(
                                [
                                    f"{'\t' * indent}board_{idx}(<img src='/board/board_{idx}.svg' width='69' height='59.4' /><br>局面{idx})"
                                    for idx in groupby.get_group(move_number)["id"]
                                ]
                            )
                            + f"\n{'\t' * indent}end\n"
                        )
        else:
            nodes = (
                "\n".join(
                    [
                        f"{'\t' * indent}board_{idx}(<img src='/board/board_{idx}.svg' width='69' height='59.4' /><br>局面{idx})"
                        for idx in range(len(self.node_df))
                    ]
                )
                + "\n"
            )
            connected_node |= set(self.edge_df["to"])
        edges = "\n".join(
            [
                f"{'\t' * indent}board_{edge[1]} --> board_{edge[2]}"
                for edge in self.edge_df.itertuples()
                if edge[2] in connected_node
                if connected_node
            ]
        )
        graph_mermaid = f"""
{'\t' * indent}graph LR
{nodes}{edges}"""
        return graph_mermaid
