class AI:
    board = ""
    state_mat = []
    
    # Alpha-Beta --> generate_states --> possible_moves --> move_validation --> all_moves
    
    def convert_str_to_mat(self, state):
        return state.split('.')
    
    def __init__(self, state):
        self.board = state
        self.state_mat = self.convert_str_to_mat(self.board)
    
    def convert_mat_to_str(self, mat):
        return ".".join(mat)
    
    def return_move_tuples(self, move):
        # move: "A4 B5" ==> [(0, 3), (1, 4)] ==> [(0, 4), (1, 3)] ==> [(4, 0), (3, 1)]
        
        letter_dict = {'A': '0', 'B': '1', 'C': '2', 'D': '3', 'E': '4', 'F': '5', 'G': '6', 'H': '7'}
        move = letter_dict[move[0]] + move[1:3] + letter_dict[move[3]] + move[4:]
        mv = move.split(' ')
        start = (7 - int(mv[0][1]) + 1, int(mv[0][0]))
        end = (7 - int(mv[1][1]) + 1, int(mv[1][0]))
        move_list = []
        move_list.append(start)
        move_list.append(end)
        
        return move_list
    
    def move_is_valid(self, move):
        mv = self.return_move_tuples(move)
        
        piece_pos = mv[0]
        possible_moves = self.return_possible_moves(piece_pos)
        
        if mv[1] in possible_moves:
            return 1
        else:
            return 0
    
    def return_possible_moves(self, pos):
        # determining type :
        # empty = e
        # white_king = k
        # black_king = K
        # white_queen = q
        # black_queen = Q
        # white_rook = r
        # black_rook = R
        # white_knight = n
        # black_knight = N
        # white_bishop = b
        # black_bishop = B
        # white_pawn = p
        # black_pawn = P
        
        moves = []
        # AI moves :
        if (self.state_mat[pos[0]][pos[1]] == 'R'):
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                p = pos
                enemy_counter = 0
                while ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and ((enemy_counter == 0 and self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e')
                                                    or ('a' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'z' and
                                                            self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e' and enemy_counter == 0))):
                    if('a' <= self.state_mat[p[0]+d[0]][p[1]+d[1]] <= 'z' and self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e'):
                        enemy_counter += 1

                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'B'):
            dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
            for d in dirs:
                p = pos
                enemy_counter = 0
                while ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                        (enemy_counter == 0 and self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e')
                or ('a' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'z' and
                            self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e' and enemy_counter == 0))):
                    if ('a' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'z' and self.state_mat[p[0] + d[0]][
                            p[1] + d[1]] != 'e'):
                        enemy_counter += 1

                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'Q'):
            dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                p = pos
                enemy_counter = 0
                while ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                        (enemy_counter == 0 and self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e')
                or ('a' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'z' and
                            self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e' and enemy_counter == 0))):
                    if ('a' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'z' and self.state_mat[p[0] + d[0]][
                            p[1] + d[1]] != 'e'):
                        enemy_counter += 1

                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'K'):
            dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                p = pos
                if ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                        self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e' or 'a' <= self.state_mat[p[0] + d[0]][
                        p[1] + d[1]] <= 'z')):
                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)
        
        elif (self.state_mat[pos[0]][pos[1]] == 'N'):
            dirs = [(1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
            for d in dirs:
                p = pos
                if ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                        self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e' or 'a' <= self.state_mat[p[0] + d[0]][
                        p[1] + d[1]] <= 'z')):
                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)
        
        elif (self.state_mat[pos[0]][pos[1]] == 'P'):
            dirs = [(1, -1), (1, 1)]
            for d in dirs:
                if(0 <= pos[0]+d[0] <= 7 and 0 <= pos[1]+d[1] <= 7 and 'a' <= self.state_mat[pos[0]+d[0]][pos[1]+d[1]] <= 'z'
                   and self.state_mat[pos[0]+d[0]][pos[1]+d[1]] != 'e'):
                    moves.append((pos[0]+d[0], pos[1]+d[1]))
            if(pos[0] == 1):
                dirs = [(1, 0), (2, 0)]
                for d in dirs:
                    if (0 <= pos[0] + d[0] <= 7 and 0 <= pos[1] + d[1] <= 7 and self.state_mat[pos[0] + d[0]][pos[1] + d[1]] == 'e'):
                        moves.append((pos[0] + d[0], pos[1] + d[1]))
            else:
                dirs = [(1, 0)]
                for d in dirs:
                    if (0 <= pos[0] + d[0] <= 7 and 0 <= pos[1] + d[1] <= 7 and self.state_mat[pos[0] + d[0]][pos[1] + d[1]] == 'e'):
                        moves.append((pos[0] + d[0], pos[1] + d[1]))

        elif (self.state_mat[pos[0]][pos[1]] == 'r'):
            dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                p = pos
                enemy_counter = 0
                while ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                        (enemy_counter == 0 and self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e')
                or ('A' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'Z' and
                            self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e' and enemy_counter == 0))):
                    if ('A' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'Z' and self.state_mat[p[0] + d[0]][
                            p[1] + d[1]] != 'e'):
                        enemy_counter += 1

                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'b'):
            dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
            for d in dirs:
                p = pos
                enemy_counter = 0
                while ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                                (enemy_counter == 0 and self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e')
                        or ('A' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'Z' and
                                    self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e' and enemy_counter == 0))):
                    if ('A' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'Z' and self.state_mat[p[0] + d[0]][
                            p[1] + d[1]] != 'e'):
                        enemy_counter += 1

                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'q'):
            dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                p = pos
                enemy_counter = 0
                while ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                                (enemy_counter == 0 and self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e')
                        or ('A' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'Z' and
                                    self.state_mat[p[0] + d[0]][p[1] + d[1]] != 'e' and enemy_counter == 0))):
                    if ('A' <= self.state_mat[p[0] + d[0]][p[1] + d[1]] <= 'Z' and self.state_mat[p[0] + d[0]][
                            p[1] + d[1]] != 'e'):
                        enemy_counter += 1

                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'k'):
            dirs = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
            for d in dirs:
                p = pos
                if ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                                self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e' or 'A' <= self.state_mat[p[0] + d[0]][
                                p[1] + d[1]] <= 'Z')):
                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'n'):
            dirs = [(1, 2), (-1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, 1), (-2, -1)]
            for d in dirs:
                p = pos
                if ((0 <= p[0] + d[0] <= 7) and (0 <= p[1] + d[1] <= 7) and (
                                self.state_mat[p[0] + d[0]][p[1] + d[1]] == 'e' or 'A' <= self.state_mat[p[0] + d[0]][
                                p[1] + d[1]] <= 'Z')):
                    p = (p[0] + d[0], p[1] + d[1])
                    moves.append(p)

        elif (self.state_mat[pos[0]][pos[1]] == 'p'):
            dirs = [(-1, 1), (-1, -1)]
            for d in dirs:
                if (0 <= pos[0] + d[0] <= 7 and 0 <= pos[1] + d[1] <= 7 and 'A' <= self.state_mat[pos[0] + d[0]][
                        pos[1] + d[1]] <= 'Z'
                    and self.state_mat[pos[0] + d[0]][pos[1] + d[1]] != 'e'):
                    moves.append((pos[0] + d[0], pos[1] + d[1]))
            if (pos[0] == 6):
                dirs = [(-1, 0), (-2, 0)]
                for d in dirs:
                    if (0 <= pos[0] + d[0] <= 7 and 0 <= pos[1] + d[1] <= 7 and self.state_mat[pos[0] + d[0]][pos[1] + d[1]] == 'e'):
                        moves.append((pos[0] + d[0], pos[1] + d[1]))
            else:
                dirs = [(-1, 0)]
                for d in dirs:
                    if (0 <= pos[0] + d[0] <= 7 and 0 <= pos[1] + d[1] <= 7 and self.state_mat[pos[0] + d[0]][pos[1] + d[1]] == 'e'):
                        moves.append((pos[0] + d[0], pos[1] + d[1]))

        return moves

    def state_is_safe(self, state, is_AI):
        if(is_AI):
            start_limit, end_limit, king = 'a', 'z', 'K'
        else:
            start_limit, end_limit, king = 'A', 'Z', 'k'

        for i in range(8):
            for j in range(8):
                piece = state[i][j]
                if(piece != 'e' and start_limit <= piece <= end_limit):
                    p_moves = self.return_possible_moves((i, j))
                    for move in p_moves:
                        if(state[move[0]][move[1]] == king):
                            return False
        return True

    def update_state_with_move(self, start, end, state, is_AI):
        copy_state = state[:]
        copy_state[end[0]] = copy_state[end[0]][: end[1]] + state[start[0]][start[1]] + copy_state[end[0]][end[1] + 1:]
        copy_state[start[0]] = copy_state[start[0]][:start[1]] + 'e' + copy_state[start[0]][start[1]+1:]

        return copy_state

    def generate_next_possible_safe_states(self, state, is_AI):
        possible_states = []
        counter = 0
        for i in range(7, -1, -1):
            for j in range(7, -1, -1):
                p_type = state[i][j]
                if(p_type != 'e' and ((is_AI and 'A' <= p_type <= 'Z') or (not is_AI and 'a' <= p_type <= 'z'))):
                    possible_moves = self.return_possible_moves((i, j))
                    for move in possible_moves:
                        state_to_check = self.update_state_with_move((i, j), move, state[:], is_AI)
                        if(self.state_is_safe(state_to_check[:], is_AI)):
                            print(state_to_check, self.state_is_safe(state_to_check[:], is_AI))
                            possible_states.append(state_to_check[:])
        return possible_states

    def return_heuristic_value(self, state):
        p_values = {"p": -1, "b": -3, "r": -2, "n": -2, "q": -9, "k": -0, "e": 0,
                    "P": 1, "B": 3, "R": 2, "N": 2, "Q": 9, "K": -0}
        h_value = 0
        for i in range(8):
            for j in range(8):
                h_value += p_values[state[i][j]]
        return h_value

    def mini_max(self, node, depth, a, b, is_AI):
        final_decision = []
        if(depth == 0 or len(self.generate_next_possible_safe_states(node, is_AI)) == 0):
            return (self.return_heuristic_value(node), None)
        if (is_AI):
            best_val = -1000*1000
            for child in self.generate_next_possible_safe_states(node, is_AI):
                val = self.mini_max(child, depth - 1, a, b, not is_AI)[0]
                best_val = max([best_val, val])
                a = max([a, best_val])
                if(a >= b): break
                if(val >= best_val):
                    best_val = val
                    final_decision = child
            return (best_val, final_decision)
        else:
            best_val = +1000 * 1000
            for child in self.generate_next_possible_safe_states(node, is_AI):
                val = self.mini_max(child, depth - 1, a, b, not is_AI)[0]
                best_val = min([best_val, val])
                b = min([b, best_val])
                if(a >= b): break
                if (val <= best_val):
                    best_val = val
                    final_decision = child
            return (best_val, final_decision)

ai = AI("RNBQKBNR.qqqqqqqq.qqqqqqqq.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr")
print(ai.state_is_safe(ai.convert_str_to_mat("RNBQeBNR.qqqqeqKq.qqqqqeqq.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr"), True))