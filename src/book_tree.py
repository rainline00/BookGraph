from abc import ABC, abstractmethod
from cshogi import Board
from util import remove_moves_from_sfen

class Component(ABC):

    @property
    @abstractmethod
    def parent(self):
        pass
    

class Node(Component):
    def __init__(self, board=None, parent=None, pre_move=None, candidate_moves=None):
        self._board = board
        self._parent = parent
        self._pre_move = pre_move
        self._candidate_moves = candidate_moves
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def board(self):
        return self._board
    
    @property
    def pre_move(self):
        return self._pre_move
    
    @property
    def candidate_moves(self):
        return self._candidate_moves
    
    def append_candidate_moves(self, move):
        self._candidate_moves.append(move)
    
    @candidate_moves.deleter
    def candidate_move(self, target_move):
        self._candidate_moves.remove(target_move)
    
    @property
    def sfen_for_hash(self):
        return remove_moves_from_sfen(self._board.sfen())


class Move():
    def __init__(self, sfen: str, chosen_move_code: str, expected_next_move_code: str, evaluation_value: int, metadata: dict[str, any] = None):
        self._sfen = sfen
        self._chosen_move_code = chosen_move_code
        self._expected_next_move_code = expected_next_move_code
        self._evaluation_value = evaluation_value
        self._metadata = metadata

    @property
    def sfen(self):
        return self._sfen
    
    @property
    def chosen_move_code(self):
        return self._chosen_move_code
    
    @property 
    def expected_next_move_code(self):
        return self._expected_next_move_code
    
    @property
    def evaluation_value(self):
        return self._evaluation_value
    
    @property
    def metadata(self):
        return self._metadata
    
    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @property
    def next_sfen(self):
        return self._next_sfen
    
    @property
    def next_sfen(self):
        board = Board(self._sfen)
        board.push_usi(self._chosen_move_code)
        return board.sfen()
    
    @property
    def sfen_for_hash(self):
        return remove_moves_from_sfen(self._sfen)
    
    @property
    def next_sfen_for_hash(self):
        return remove_moves_from_sfen(self.next_sfen)