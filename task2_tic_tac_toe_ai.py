import tkinter as tk
from tkinter import messagebox
import math
board = [' ' for _ in range(9)]
buttons = []
def check_winner(brd, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]           
    ]
    for cond in win_conditions:
        if brd[cond[0]] == brd[cond[1]] == brd[cond[2]] == player:
            return True
    return False
def is_full(brd):
    return ' ' not in brd
def minimax(brd, depth, is_maximizing):
    if check_winner(brd, 'O'):
        return 1
    elif check_winner(brd, 'X'):
        return -1
    elif is_full(brd):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if brd[i] == ' ':
                brd[i] = 'O'
                score = minimax(brd, depth + 1, False)
                brd[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if brd[i] == ' ':
                brd[i] = 'X'
                score = minimax(brd, depth + 1, True)
                brd[i] = ' '
                best_score = min(score, best_score)
        return best_score


def ai_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    if move != -1:
        board[move] = 'O'
        buttons[move].config(text='O', state='disabled')
        check_game_over()
def check_game_over():
    if check_winner(board, 'X'):
        messagebox.showinfo("Game Over", "You win!")
        reset_game()
    elif check_winner(board, 'O'):
        messagebox.showinfo("Game Over", "AI wins!")
        reset_game()
    elif is_full(board):
        messagebox.showinfo("Game Over", "It's a tie!")
        reset_game()
def on_click(index):
    if board[index] == ' ':
        board[index] = 'X'
        buttons[index].config(text='X', state='disabled')
        check_game_over()
        if not is_full(board) and not check_winner(board, 'X'):
            ai_move()
def reset_game():
    global board
    board = [' ' for _ in range(9)]
    for btn in buttons:
        btn.config(text=' ', state='normal')
root = tk.Tk()
root.title("Tic Tac Toe - AI")
for i in range(9):
    button = tk.Button(root, text=' ', font=('Arial', 24), width=5, height=2,
                       command=lambda i=i: on_click(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)
reset_button = tk.Button(root, text="Reset", font=('Arial', 14), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, pady=10)
root.mainloop()
