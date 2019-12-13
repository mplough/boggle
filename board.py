from collections import defaultdict
import pathlib
from random import randint, shuffle

import click

# There is a 4x4 board with 16 6-sided letter dice.
# Dice distributions from
# http://www.bananagrammer.com/2013/10/the-boggle-cube-redesign-and-its-effect.html.
CLASSIC_DICE = (
    ('A', 'A', 'C', 'I', 'O', 'T',),
    ('A', 'B', 'I', 'L', 'T', 'Y',),
    ('A', 'B', 'J', 'M', 'O', 'QU',),
    ('A', 'C', 'D', 'E', 'M', 'P',),
    ('A', 'C', 'E', 'L', 'R', 'S',),
    ('A', 'D', 'E', 'N', 'V', 'Z',),
    ('A', 'H', 'M', 'O', 'R', 'S',),
    ('B', 'I', 'F', 'O', 'R', 'X',),
    ('D', 'E', 'N', 'O', 'S', 'W',),
    ('D', 'K', 'N', 'O', 'T', 'U',),
    ('E', 'E', 'F', 'H', 'I', 'Y',),
    ('E', 'G', 'K', 'L', 'U', 'Y',),
    ('E', 'G', 'I', 'N', 'T', 'V',),
    ('E', 'H', 'I', 'N', 'P', 'S',),
    ('E', 'L', 'P', 'S', 'T', 'U',),
    ('G', 'I', 'L', 'R', 'U', 'W',),
)

NEW_DICE = (
    ('A', 'A', 'E', 'E', 'G', 'N',),
    ('A', 'B', 'B', 'J', 'O', 'O',),
    ('A', 'C', 'H', 'O', 'P', 'S',),
    ('A', 'F', 'F', 'K', 'P', 'S',),
    ('A', 'O', 'O', 'T', 'T', 'W',),
    ('C', 'I', 'M', 'O', 'T', 'U',),
    ('D', 'E', 'I', 'L', 'R', 'X',),
    ('D', 'E', 'L', 'R', 'V', 'Y',),
    ('D', 'I', 'S', 'T', 'T', 'Y',),
    ('E', 'E', 'G', 'H', 'N', 'W',),
    ('E', 'E', 'I', 'N', 'S', 'U',),
    ('E', 'H', 'R', 'T', 'V', 'W',),
    ('E', 'I', 'O', 'S', 'S', 'T',),
    ('E', 'L', 'R', 'T', 'T', 'Y',),
    ('H', 'I', 'M', 'N', 'U', 'QU',),
    ('H', 'L', 'N', 'N', 'R', 'Z',),
)

WORDS_FILE = pathlib.Path(__file__).parent / 'Collins Scrabble Words (2015).txt'


def load_words(filename):
    with open(filename) as f:
        all_words = [
            line.upper().strip()
            for line in f
        ]

    valid_words = {w for w in all_words if 3 <= len(w) <= 16}
    print(f'There are {len(valid_words)} words in the database.')
    return valid_words


def filter_words(words, board):
    board_letters = set(''.join([
        node.letter
        for row in board
        for node in row
    ]))
    filtered_words = [w for w in words if not (set(w) - board_letters)]
    print(f'At most {len(filtered_words)} can be found.')
    return filtered_words


def set_up(dice):
    """Create a Boggle board, letters only."""
    letters = [die[randint(0, 5)] for die in dice]
    shuffle(letters)

    board = [
        letters[i:i+4]
        for i in range(0, len(letters), 4)
    ]
    return board


def read_board(board_str):
    letters = board_str.split()
    board = [
        letters[i:i+4]
        for i in range(0, len(letters), 4)
    ]
    return board


class Node:
    def __init__(self, letter):
        self.letter = letter
        self.metadata = defaultdict(list)
        self.visited = False

    def __str__(self):
        str_metadata = ','.join(f'({k}: {v})' for k, v in self.metadata.items())
        letter = self.letter.lower() if self.visited else self.letter
        return f'{letter}: {str_metadata}'

    def __repr__(self):
        return str(self)


def add_metadata(board):
    """Add metadata to the Boggle board.

    We have a hybrid graph/trie data structure.
    """

    root = Node('')
    for r, row in enumerate(board):
        for c, letter in enumerate(row):
            board[r][c] = Node(letter)

    # holy crap I'm a lazy thinker
    for r, row in enumerate(board):
        for c, node in enumerate(row):
            root.metadata[node.letter].append((r, c))
            adjacencies = [
                (r-1, c-1),
                (r-1, c),
                (r-1, c+1),
                (r,   c-1),
                (r,   c+1),
                (r+1, c-1),
                (r+1, c),
                (r+1, c+1),
            ]
            for (adj_r, adj_c) in adjacencies:
                if 0 <= adj_r < len(board) and 0 <= adj_c < len(row):
                    adj_letter = board[adj_r][adj_c].letter
                    board[r][c].metadata[adj_letter].append((adj_r, adj_c))
    return root, board


def str_board(board):
    return '\n'.join(
        ' '.join(
            '{:<2}'.format(node.letter.lower() if node.visited else node.letter)
            for node in row
        )
        for row in board
    )


def clear(root, board):
    root.visited = False
    for row in board:
        for node in row:
            node.visited = False


def traverse(word, root, board):
    visited = root.visited
    root.visited = True
    root.visited = visited

    if root.visited:
        return False

    root.visited = True

    if root.letter == word:
        return True

    new_word = word[len(root.letter):]
    for letter, node_indices in root.metadata.items():
        if new_word.startswith(letter):
            for node_index in node_indices:
                node = board[node_index[0]][node_index[1]]
                if traverse(new_word, node, board):
                    return True
    root.visited = False
    return False


@click.command()
@click.option('--board-filename')
@click.option('--word')
def click_main(board_filename, word):
    if board_filename:
        with open(board_filename) as f:
            contents = f.read()
            letters = read_board(contents)
    else:
        letters = set_up(NEW_DICE)

    root, board = add_metadata(letters)

    valid_words = load_words(WORDS_FILE)
    filtered_words = filter_words(valid_words, board)

    if word:
        word = word.upper()
        if word not in valid_words:
            print(f'"{word}" is not a valid word.')
            return
        print(traverse(word, root, board))

    else:
        print(str_board(board))
        print()
        n = 0
        for w in sorted(filtered_words):
            clear(root, board)
            if traverse(w, root, board):
                n += 1
                print(w)
        print(f'{n} words were found.')


if __name__ == '__main__':
    click_main()
