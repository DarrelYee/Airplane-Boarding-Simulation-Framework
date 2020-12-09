import random

SEAT_LETTERS = 'ABCDEF'

class Passenger:
    '''
    This is the base class representing a passenger.
    Initialize with the passenger's row number and seat alphabet (denote with the respective digit during initialization).
    If randomize_stowing argument is True, the passenger may be randomly assigned as a slow stower.
    A slow stower takes two steps to stow instead of one.
    '''
    
    def __init__(self, row, seat, randomize_stowing = True):
        if randomize_stowing:
            self.slow = bool(random.randint(0,1))
        else:
            self.slow = False
        self.row = row
        self.seat = seat
        self.storing = False
        self.storing_slow = False
        global SEAT_LETTERS
        self.string = str(self.row) + SEAT_LETTERS[self.seat]

    def __repr__(self):
        return self.string
