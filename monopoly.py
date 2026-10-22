"""
Monopoly Phase 1
CS 310 - Intro to Python Programming

Roll the dice and move around the board.
Two players alternate turns for 20 turns.
Not object oriented yet: each player is a list.
"""

import random

# Uncomment the next line to repeat the same game while debugging
# random.seed(5)

# Indexes into each player list
NAME, MONEY, LOCATION = 0, 1, 2
DOUBLES, IN_JAIL, JAIL_CARDS = 3, 4, 5

# Special space numbers on the board (0 - 39)
GO = 0
INCOME_TAX = 4
JAIL = 10
GO_TO_JAIL = 30
LUXURY_TAX = 38


bank = 0  # money paid to the Bank (taxes, jail fees)


def load_board(filename):
    """Read board.txt into a list of (name, description) tuples.
    Line 1 of the file is space 0 (GO)."""
    board = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            name, desc = line.split("|")
            board.append((name, desc))
    return board


def roll_die():
    """One die: a whole number from 1 to 6."""
    return random.randint(1, 6)


def move_player(player, roll, board):
    """Add the roll to the player's location, wrapping around the board.
    Collect $200 whenever the move passes or lands on GO."""
    if player[LOCATION] + roll >= 40:
        player[MONEY] += 200
        print("Collects $200 for passing GO")
    player[LOCATION] = (player[LOCATION] + roll) % 40
    print("Moves to:", player[LOCATION], board[player[LOCATION]][0])


def handle_space(player, board):
    """Apply the rule for the space the player just landed on."""
    global bank
    if player[LOCATION] == INCOME_TAX:
        # Pay the Bank 10% of your money, but never more than $200
        tax = int(player[MONEY] * 0.10)
        if tax > 200:
            tax = 200
        player[MONEY] -= tax
        bank += tax
        print("Pays $%d in Income Tax" % tax)
    elif player[LOCATION] == LUXURY_TAX:
        # Pay the Bank a flat $75
        player[MONEY] -= 75
        bank += 75
        print("Pays $75 in Luxury Tax")
    elif player[LOCATION] == GO_TO_JAIL:
        # Go directly to Jail, do not pass GO
        player[LOCATION] = JAIL
        player[IN_JAIL] = True
        player[DOUBLES] = 0
        print(player[NAME], "goes to Jail!")


def take_turn(player, board):
    """Play one full turn: roll, move, follow the rules, print what happened."""
    print("---  %s's turn  ---" % player[NAME])

    global bank

    if player[IN_JAIL]:
        # Getting out of Jail (Phase 1): pay $50 to the Bank,
        # then roll and move.
        player[IN_JAIL] = False
        player[MONEY] -= 50
        bank += 50
        print("Pays $50 to get out of Jail")

    while True:
        die1 = roll_die()
        die2 = roll_die()
        print("die 1:", die1, "  die 2:", die2)

        if die1 == die2:
            # A double: keep a count of consecutive doubles
            player[DOUBLES] += 1

            if player[DOUBLES] == 3:
                # Double # 3: go to Jail instead of moving
                player[LOCATION] = JAIL
                player[IN_JAIL] = True
                player[DOUBLES] = 0
                print("Double # 3")
                print(player[NAME], "goes to Jail!")
                break

            print("Double # %d" % player[DOUBLES])
            move_player(player, die1 + die2, board)
            handle_space(player, board)
            if player[IN_JAIL]:
                # Landed on Go To Jail: the turn is over
                break
            print("Rolls again!")
        else:
            # Any roll that is not a double ends the turn,
            # and resets the doubles count to 0
            player[DOUBLES] = 0
            move_player(player, die1 + die2, board)
            handle_space(player, board)
            break

    print("Money: $%d" % player[MONEY])


def main():
    board = load_board("board.txt")

    # Each player: name, money, location, doubles, in jail, jail cards
    player1 = ["Player 1", 1500, 0, 0, False, 0]
    player2 = ["Player 2", 1500, 0, 0, False, 0]

    # The game loop: 20 turns, players alternate
    for turn in range(1, 21):
        if turn % 2 == 1:
            current = player1
        else:
            current = player2

        print("Turn", turn)
        take_turn(current, board)
        print()


if __name__ == "__main__":
    main()
