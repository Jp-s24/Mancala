#------------------------------------------------------
# Name: Jean-Paul Saliba
# Student Id: 100741759
#------------------------------------------------------
#      HackerRank Mancala Solution
#------------------------------------------------------

#function containing the 5 parameters as requested per HackerRank
def printNextMove(player, player1Mancala, player1Marbles, player2Mancala, player2Marbles):
    if player == '1':
        marbles = player1Marbles
        score = player1Mancala
        Opponent_Marbles = player2Marbles
        Opponent_Score = player2Mancala
    elif player == '2':
        marbles = player2Marbles
        score = player2Mancala
        Opponent_Marbles = player1Marbles
        Opponent_Score = player1Mancala

    #create the board
    board = Construct_Board(marbles, score, Opponent_Marbles, Opponent_Score)
    First_Turn = [2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 0]
    Second_Turn = [3, 3, 0, 6, 6, 6, 1, 3, 3, 3, 3, 3, 3, 0]
    Third_Turn = [4, 0, 5, 5, 4, 4, 1, 4, 4, 0, 4, 4, 0, 2]

    # optimal turn 1 moves
    if board == First_Turn:
        print(3)
    elif board == Second_Turn:
        print(6)
    elif board == Third_Turn:
        print(1)
    else:
        select = Alpha_Beta_Minimax(board, True, 8, -10000, 10000)
        print(select[1])


# Function that constructs the Mancala board
def Construct_Board(marbles, score, Opponent_Marbles, Opponent_Score):
    board = []
    for x in marbles:
        board.append(x)

    board.append(int(score))

    for x in Opponent_Marbles:
        board.append(x)

    board.append(int(Opponent_Score))

    return board

#Function that gets the score
def Retrieve_Score(board, end, depth, maxPlayer):
    if (sum(board[:7]) > sum(board[7:]) and end) or board[6] > 24:
        score = 1000 + depth
    elif (sum(board[:7]) < sum(board[7:]) and end) or board[13] > 24:
        score = -1000 + depth
    else:
        score = (board[6] - board[13]) * 3 + (sum(board[:7]) - sum(board[7:]))

    return score


# Find possible moves from a given board state
def Locate_Moves(board, Highest_Player):
    moves = []
    for i in range(6):
        if Highest_Player:
            if board[i] != 0:
                moves.append(i)
        else:
            if board[i + 7] != 0:
                moves.append(i)

    return moves


# Alpha beta pruning Minimax algorithm which checks for all possible cases then find highest score possible
def Alpha_Beta_Minimax(board, maxPlayer, depth, alpha, beta):
    finish = Status_Of_Game_Check(board)
    if depth == 0 or finish:
        score = Retrieve_Score(board, finish, depth, maxPlayer)

        return score, None

    if maxPlayer:
        Optimal_Score = -100000000
        move = None
        # Calls minimax for all the 6 possible moves
        for i in range(6):
            if board[i] != 0:
                # Locates next state when a move is chosen
                Next_Board = Get_Next_State(i + 1, board.copy(), maxPlayer)

                # checks if rival gets an extra turn
                if Next_Board[1]:
                    score = Alpha_Beta_Minimax(Next_Board[0], Next_Board[1], depth, alpha, beta)
                else:
                    score = Alpha_Beta_Minimax(Next_Board[0], Next_Board[1], depth - 1, alpha, beta)

                if score[0] > Optimal_Score:
                    Optimal_Score = score[0]
                    move = i + 1

                alpha = max(alpha, Optimal_Score)
                # perform Alpha beta pruning
                if beta <= alpha:
                    break

        return Optimal_Score, move

    else:
        Optimal_Score = 10000
        move = None
        # Calls minimax for all the 6 possible moves
        for i in range(6):
            if board[i + 7] != 0:
                # Locates the next state when a move is chosen
                Next_Board = Get_Next_State(i + 8, board.copy(), maxPlayer)
                # checks if the rival gets an extra turn
                if Next_Board[1] == False:
                    score = Alpha_Beta_Minimax(Next_Board[0], Next_Board[1], depth, alpha, beta)
                else:
                    score = Alpha_Beta_Minimax(Next_Board[0], Next_Board[1], depth - 1, alpha, beta)

                if score[0] < Optimal_Score:
                    Optimal_Score = score[0]
                    move = i + 8
                beta = min(beta, Optimal_Score)
                # perform Alpha beta pruning
                if beta <= alpha:
                    break
        return Optimal_Score, move


# Gets the future state of the board
def Get_Next_State(pick, board, maxPlayer):
    moves = board[pick - 1]
    board[pick - 1] = 0
    k = pick

    # create Default value of extra
    if maxPlayer:
        extra = False
    else:
        extra = True

    while moves > 0:
        if k >= len(board):
            k = 0
        if moves == 1 and board[k] == 0 and k != 6 and k != 13:
            board[k] = board[12 - k]
            board[12 - k] = 0

        # Extra turn
        if moves == 1:
            if maxPlayer and k == 6:
                extra = True
            elif maxPlayer == False and k == 13:
                extra = False

        # Skips over the opponents Mancala
        if maxPlayer and k != 13:
            board[k] += 1
            moves -= 1
        elif maxPlayer == False and k != 6:
            board[k] += 1
            moves -= 1

        k += 1

    return board, extra


# function that checks if the game is won or losr
def Status_Of_Game_Check(board):
    if sum(board[:6]) == 0 or sum(board[7:13]) == 0:
        return True
    else:
        return False

#main function
def main():
    # read input given
    player = input()
    mancala1 = input()
    mancala1_marbles = [int(i) for i in input().strip().split()]
    mancala2 = input()
    mancala2_marbles = [int(i) for i in input().strip().split()]
    # call the function with the input values to produce the desired output
    printNextMove(player, mancala1, mancala1_marbles, mancala2, mancala2_marbles)
#calls the main function
main()