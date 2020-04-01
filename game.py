class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    ROWS = 6
    COLUMNS = 7
    CHECK_FACTOR = 3
    '''
    I assigned it to be equal to 3 because in the functions where I check if there is a winner,
    I use the number 3 constantly
    '''

    def __init__(self):
        '''
        Initializes the class Game. It has all the algorithms to run the game without the design,
        such as finding the next legal move, check if there is a winner or not...
        '''
        self.winner_dict = []  # Holds the coordinates of the winning player
        self.counter = 0
        self.coord_table = {}
        for index_row in range(self.ROWS):
            for index_col in range(self.COLUMNS):
                coord = index_row, index_col
                self.coord_table[coord] = None

    def column_is_full(self, column):
        '''

        :param column: Takes in column from the board
        :return: Returns False if the column is still not full, else it raises an exception if it is
        '''
        if self.coord_table[(0, column)] == None:
            return False
        else:
            raise Exception('Illegal move\n')
            return True

    def Index_last_none(self, column):
        '''

        :param column: Takes in column from the board
        :return: Returns the coordinates of the legal assignment
        '''
        rows = self.ROWS - 1
        while rows >= 0:
            if self.coord_table[(rows, column)] == None:
                return (rows, column)
            rows -= 1

    def make_move(self, column):
        '''

        :param column: Takes in column from the board
        :return: Returns the player that did the move with the coordinates of the assignment(legal move)
        '''
        check = True
        while check:
            try:
                if not self.column_is_full(column):
                    coord_place = self.Index_last_none(column)
                    if self.counter % 2 == 0:
                        self.coord_table[coord_place] = self.PLAYER_ONE
                        self.counter += 1
                        return self.PLAYER_ONE, coord_place
                    else:
                        self.coord_table[coord_place] = self.PLAYER_TWO
                        self.counter += 1
                        return self.PLAYER_TWO, coord_place
            except:
                ('Illegal move. Insert again\n')
                return False
            self.counter += 1

    def get_pre_player(self):
        '''

        :return: Returns the player that played in the last round
        '''
        if self.counter % 2 == 0:
            return self.PLAYER_TWO
        if self.counter % 2 == 1:
            return self.PLAYER_ONE

    def check_if_full(self):
        '''

        :return: Returns True if the board is full, else False
        '''
        for column in range(self.COLUMNS):
            if self.coord_table[(0, column)] == None:
                return False
        return True

    def check_horizontal(self, row, col):
        '''

        :param row: Takes a row from the board
        :param col: Takes a column from the board
        :return: Returns True if the player one horizontally, else False
        '''
        if self.coord_table[(row, col)] == None:
            return False
        if col in range(self.CHECK_FACTOR + 1, self.COLUMNS):  # Not in the range to win horizontally
            return False
        color_player = self.coord_table[(row, col)]  # Disk of the current player
        column = col
        while column <= col + self.CHECK_FACTOR:
            self.winner_dict.append((row, column))  # We use this list so we can change the winner's disks
            if self.coord_table[(row, column)] != color_player and color_player != None:
                self.winner_dict = []
                return False
            column += 1

        return True

    def check_parallel(self, row, col):
        '''

        :param row: Row from the board
        :param col: Column from the board
        :return: Returns True if the player one in a parallel way
        '''
        if self.coord_table[(row, col)] == None:
            return False
        if row >= self.ROWS - self.CHECK_FACTOR:  # Not in the range to win in that way
            return False
        color_player = self.coord_table[(row, col)]  # Disk of the current player
        rows = row
        while rows <= row + self.CHECK_FACTOR:
            self.winner_dict.append((rows, col))  # We use this list so we can change the winner's disks
            if self.coord_table[(rows, col)] != color_player and color_player != None:
                self.winner_dict = []
                return False
            rows += 1
        return True

    def check_diagonal(self, row, col):
        '''

        :param row: Row from the board
        :param col: Column from the board
        :return: Returns True if the player one diagonally
        '''
        if self.coord_table[(row, col)] == None:
            return False
        if row in range(0, self.ROWS) and col in range(self.CHECK_FACTOR + 1, self.COLUMNS):  # Not in the right range
            return False
        color_player = self.coord_table[(row, col)]
        rows = row
        columns = col
        '''
        Here there is two ways to win diagonally, either in the range (0,3) - (0,4), or
        (3,6) - (0,4) 
        '''
        if row in range(0, self.CHECK_FACTOR) and col in range(0, self.CHECK_FACTOR + 1):  # In the right range
            while rows <= row + self.CHECK_FACTOR and columns <= col + self.CHECK_FACTOR:
                self.winner_dict.append((rows, columns))  # We use this list so we can change the winner's disks
                if self.coord_table[(rows, columns)] != color_player and color_player != None:
                    self.winner_dict = []
                    return False
                rows += 1;
                columns += 1
        if row in range(self.CHECK_FACTOR, self.ROWS) and col in range(0, self.CHECK_FACTOR + 1):  # In the right range
            while rows >= row - self.CHECK_FACTOR and columns <= col + self.CHECK_FACTOR:
                self.winner_dict.append((rows, columns))  # We use this list so we can change the winner's disks
                if self.coord_table[(rows, columns)] != color_player and color_player != None:
                    self.winner_dict = []
                    return False
                rows -= 1;
                columns += 1
        return True

    def get_winner(self):
        '''

        :return: Returns the winning player, else returns DRAW
        '''

        for row in range(self.ROWS):
            for column in range(self.COLUMNS):
                if self.check_horizontal(row, column):
                    player = (self.get_current_player() + 1) % 2
                    return player
                if self.check_parallel(row, column):
                    player = (self.get_current_player() + 1) % 2
                    return player
                if self.check_diagonal(row, column):
                    player = (self.get_current_player() + 1) % 2
                    return player
        if not self.check_if_full():
            return self.DRAW

    def get_player_at(self, row, col):
        '''

        :param row: Row from the board
        :param col: Column form the board
        :return: Returns the player that is found in the place (row, col)
        '''
        return self.coord_table[(row, col)]

    def get_current_player(self):
        '''

        :return: Returns the player that is holding the current turn
        '''
        if self.counter % 2 == 0:
            return self.PLAYER_ONE
        if self.counter % 2 == 1:
            return self.PLAYER_TWO
