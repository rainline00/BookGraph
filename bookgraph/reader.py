from bookgraph.book_tree import Move, Node
from pathlib import Path
from typing import Generator
from cshogi import Board


class YaneuraBookReader:
    @classmethod
    def from_generator(cls, generator: Generator[str, any, any]):
        board = Board(next(generator).lstrip("sfen ").rstrip())
        candidate_moves = []
        for line in generator:
            if line.startswith("sfen"):
                yield Node(board=board, candidate_moves=candidate_moves)
                board = Board(line.lstrip("sfen ").rstrip())
                candidate_moves = []
            else:
                data = line.rstrip().split()
                assert len(data) >= 3
                move = Move(
                    sfen=board.sfen(),
                    chosen_move_code=data[0],
                    expected_next_move_code=data[1],
                    evaluation_value=data[2],
                )
                # TODO: metadataのkeyを設定する
                if len(data) == 4:
                    move.metadata = {"0": data[3]}
                elif len(data) > 4:
                    move.metadata = {
                        str(idx): data for idx, data in enumerate(data[3:])
                    }
                candidate_moves.append(move)
        else:
            yield Node(board=board, candidate_moves=candidate_moves)

    @classmethod
    def from_str(cls, content: str):
        yield from cls.from_generator((content.splitlines()))

    @classmethod
    def from_file(cls, path: Path | str):
        if isinstance(path, str):
            path = Path(path)
        assert isinstance(path, Path)
        with open(path, mode="r") as f_db:
            yield from cls.from_generator(f_db)


if __name__ == "__main__":
    path = Path("/workspaces/BookGraph/data/book.db")
    nodes = list(YaneuraBookReader.from_file(path))
    for node in nodes[:5]:
        # print(node.candidate_moves[0].sfen)
        # print(node.candidate_moves[0].chosen_move_code)
        # print(node.candidate_moves[0].next_sfen)
        print(node.sfen_for_hash)
        print(node.candidate_moves[0].next_sfen)
        print(node.candidate_moves[0].next_sfen_for_hash)
        print()
