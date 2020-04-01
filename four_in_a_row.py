MAXIMUM_PORT = 65535
MIN_PORT = 1000
IS_AI = 'ai'
IS_HUMAN = 'human'
import sys
import GUI_Code


def main_helper(argv):
    '''

    :param argv: Arguments for the main program
    :return: Checks if the arguments given to the main are legal and can be dealt with
    '''
    if len(argv) < 3 or len(argv) > 4:  # The Parameters are missing or too much
        return False
    elif argv[1] != IS_AI and argv[1] != IS_HUMAN:  # The first object should be whether it is ai or human
        return False
    elif int(argv[2]) > MAXIMUM_PORT or int(argv[2]) < MIN_PORT:  # The inserted port is incorrect
        return False
    else:
        return True


def main_program(argv):
    '''

    :param argv: Arguments for the main project
    :return: Deals with arguments and assigns them in the right places
    '''

    if main_helper(argv) and len(sys.argv) == 4:
        game_type = argv[1]
        port = int(argv[2])
        ip = argv[3]
        gui_board = GUI_Code.GUI(game_type, port, ip)
        return
    if main_helper(argv) and len(sys.argv) == 3:
        game_type = argv[1]
        port = int(argv[2])
        ip = None
        gui_board = GUI_Code.GUI(game_type, port, ip)
        return
    else:
        print('Illegal program arguments')


if __name__ == '__main__':
    main_program(sys.argv)
