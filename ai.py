import random


class AI:
    def find_legal_move(self, g, func, timeout=None):
        '''

        :param g: An object with class type Game
        :param func: Function to assign an assignment
        :param timeout: ...
        :return:
        '''
        check = True
        while check:
            col_random = random.randrange(0, 7)
            if g.coord_table[(0, col_random)] == None or g.check_if_full():
                check = False
        func(col_random)

