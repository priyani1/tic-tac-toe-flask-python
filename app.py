from flask import Flask, render_template, request
import random

app = Flask(__name__)

board = [''] * 9
win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
]

def check_winner(board, player):
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

def bot_move(board):
        player_coords = [i for i, spot in enumerate(board) if spot == 'X']
        empty_spots = [i for i, spot in enumerate(board) if spot == '']
        for line in win_conditions:
            bot_count = sum(1 for pos in line if board[pos] == 'O')
            empty_count = sum(1 for pos in line if board[pos] == '')
            if bot_count == 2 and empty_count == 1:
                spot = next(pos for pos in line if board[pos] == '')
                board[spot] = 'O'
                return
            
        for line in win_conditions:
            player_count = sum(1 for pos in line if board[pos] == 'X')
            empty_count = sum(1 for pos in line if board[pos] == '')
            if player_count == 2 and empty_count == 1:
                spot = next(pos for pos in line if board[pos] == '')
                board[spot] = 'O'
                return
        
        if empty_spots:
            spot = random.choice(empty_spots)
            board[spot] = 'O'

@app.route('/', methods=['GET', 'POST'])
def game():
    global board
    message = ""
    devInfo = {}
    clicked = False

    if request.method == 'POST':
        for i in range(9):
            board[i] = request.form.get(f'cell{i}', '').upper()
        if check_winner(board, 'X'):
            message = "You win!"
        elif '' not in board:
            message = "It's a tie!"
        else:
            bot_move(board)
            if check_winner(board, 'O'):
                message = "Bot wins!"

    return render_template('game.html', board=board, message=message, devInfo = {}, clicked = False)

@app.route('/reset')
def reset():
    global board
    board = [''] * 9
    return render_template('game.html', board=board, message="", devInfo = {}, clicked = False)

@app.route('/showDevInfo')
def ShowDevInfo():
    return render_template('game.html', board = board, message = "", devInfo = {
        'Name': 'Priyani Kumari',
        'e-mail': 'priyanik41@gmail.com',
        'University': 'CV Raman Global University, Bhubaneswar'}, clicked = True)

if __name__ == '__main__':
    app.run(debug=True)