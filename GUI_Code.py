import game
from tkinter import *
from communicator import *
from ai import *
from PIL import ImageTk


class GUI:
    '''
    Here it initializes the first step of the board and the game itself. Assigning the images by uploading them,
    creates the frame of the board, assigns some important objects we will be using throughout the game
    '''
    player_dict = {}
    red_ball = 'red_ball.jpeg'
    blue_ball = 'blue_ball.jpeg'
    circle = 'black_circle.jpg'
    winner = 'winner_ball.jpeg'
    screen = Tk()
    frame = Frame(screen, width=700, height=600)
    frame_status = Frame(screen, width=700, height=100)
    frame_status.pack(side=TOP)
    frame.pack(side=BOTTOM)
    screen.title("4 In A Row")
    screen.resizable(0, 0)
    coord_table = {}
    count = 0
    image_none = ImageTk.PhotoImage(ImageTk.Image.open(circle))
    image_player_one = ImageTk.PhotoImage(ImageTk.Image.open(red_ball))
    image_player_two = ImageTk.PhotoImage(ImageTk.Image.open(blue_ball))
    image_winner = ImageTk.PhotoImage(ImageTk.Image.open(winner))

    def __init__(self, type, port, ip):
        '''

        :param type: Type of the player that will be playing, either ai(artificial intelligence) or human.
        Here we initialize everything, from creating the grid to connecting the board with each other, assign
        disk according to the players and returns the winner or DRAW otherwise...
        '''
        self.button_dict = {}
        self.full = False
        self.game_flag = True
        self.my_ip = ip
        self.port = port
        if self.my_ip == None:
            self.communicator = Communicator(self.screen, self.port)
        else:
            self.communicator = Communicator(self.screen, self.port, self.my_ip)
        self.communicator.connect()
        self.communicator.bind_action_to_message(self.receive_message)
        self.game_obj = game.Game()
        self.player_dict[self.game_obj.PLAYER_ONE] = self.image_player_one
        self.player_dict[self.game_obj.PLAYER_TWO] = self.image_player_two
        # Start calling the main functions to play 4 in a row
        self.status = Label(self.frame_status, text='Player 0 turn', font=('coronet', 20))
        self.status.pack()
        self.check = True
        self.game_type = type
        self.my_ai = AI()
        self.create_grid()
        self.screen.mainloop()

    def sending_connecting(self, col):
        '''

        :param col: A column we want to check and assign
        :return: Deals with the assignments of the board by either raising an exception or assigning
        a legal move on to the board
        '''

        try:
            if self.check == False:
                self.status.config(
                    text='Illegal Move! ' + 'Player ' + str(self.game_obj.get_pre_player()) + ' already won!')
                return
            if self.game_flag:
                if not self.game_obj.column_is_full(col):
                    Communicator.send_message(self.communicator, str(col))
                    self.press_button(col)
                    self.game_flag = False
            else:
                self.status.config(text='Not your turn')
        except:
            self.status.config(text='Illegal move. ' + 'Player ' + \
                                    str(self.game_obj.get_current_player()) + ' ,insert again.')

    def assign_player(self, player, button):
        '''

        :param player: Player we want to assign on to the board
        :param button: Button we want to change it's image to the image associated with the current player
        :return: Assigns player's disk in where he pressed
        '''
        if player == self.game_obj.PLAYER_ONE:
            button.config(image=self.image_player_one)
            player = self.game_obj.get_winner()
            if player == self.game_obj.PLAYER_ONE:
                self.assign_winner(player)
                return
            self.count += 1
            self.status.config(
                text='Player ' + str(self.game_obj.get_current_player()) + ' turn')
            return
        else:
            button.config(image=self.image_player_two)
            player = self.game_obj.get_winner()
            if player == self.game_obj.PLAYER_TWO:
                self.assign_winner(player)
                return
            self.count += 1
            self.status.config(
                text='Player ' + str(self.game_obj.get_current_player()) + ' turn')
            return

    def assign_winner(self, player):
        '''

        :param player: Player that won
        :return: Changes the image of the player's disk into winning disks
        '''
        for index in range(len(self.game_obj.winner_dict)):
            temp_button = Button(self.frame, image=self.image_winner)
            temp_button.grid(row=self.game_obj.winner_dict[index][0],
                             column=self.game_obj.winner_dict[index][1])
        self.status.config(text='Player ' + str(player) + ' won!')
        self.check = False
        return

    def press_button(self, col):
        '''

        :param col: A column we want to check and assign
        :return: Deals with everything that has to do with assignments. Where it calls the functions
        from the class Game and checks if it is legal to assign here or not, if the game ended with a draw, if a player
        won, if it is legal to assign in this column or continue after a player has already won.
        '''
        if self.check == False:
            self.status.config(
                text='Illegal Move! ' + 'Player ' + str(self.game_obj.get_pre_player()) + ' already won!')
            return
        while not self.full:  # Still not full
            try:
                if not self.game_obj.column_is_full(col) and not self.full:
                    situation = self.game_obj.make_move(col)
                    if self.game_obj.check_if_full():
                        temp_button = Button(self.frame, image=self.player_dict[situation[0]])
                        temp_button.grid(row=situation[1][0], column=situation[1][1])
                        self.status.config(text='Game ended with a draw!')
                        self.full = True
                        return
                    if situation != False:
                        try:
                            if self.game_flag:
                                button = self.button_dict[situation[1]]
                                self.assign_player(situation[0], button)
                                return
                        except:
                            self.status.config(text='Not your turn')
                            return
            except:
                self.status.config(text='Illegal move. ' + 'Player ' + \
                                        str(self.game_obj.get_current_player()) + ' ,insert again.')
                return

    def receive_message(self, message):
        '''

        :param message: A message which is primarily a column
        :return: Deals with the message and assigning it
        '''
        self.game_flag = True
        self.press_button(int(message))
        if self.game_type == 'ai':
            self.my_ai.find_legal_move(self.game_obj, self.sending_connecting)
            if self.full:
                self.status.config(text='Game ended with a draw!')

    def create_grid(self):
        '''

        :return: Creates the grid for the gamers, whether for human or ai. Also it assigns commands to the buttons
        if the player is human, else it just creates them(if it was ai).
        '''
        for rows in range(6):
            for cols in range(7):
                if self.game_type != 'ai':  # To assign command to the buttons
                    temp_button = Button(self.frame, image=self.image_none, command=lambda loc=cols: \
                        self.sending_connecting(loc))
                else:
                    temp_button = Button(self.frame, image=self.image_none)  # Creates grid for ai, without command
                self.button_dict[(rows, cols)] = temp_button
                temp_button.grid(row=rows, column=cols)
        if self.my_ip == None and self.game_type == 'ai':  # In case it's ai vs. ai
            self.my_ai.find_legal_move(self.game_obj, self.sending_connecting)
