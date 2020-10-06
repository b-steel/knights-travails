import queue
class Board():
    def __init__(self):
        self.size = 8
        self.loc = {}
        for row in range(8):
            self.loc[row] = {}
            for col in range(8):
                self.loc[row][col] = []
    
    def on_board(self, location):
        ''' Returns if location is on the board.  location is a tuple: (x,y)'''
        return (location[0] >= 0 and location[0] < 8 and location[1] >= 0 and location[1] < 8)
            
class Knight():
    def __init__(self, position = (0,0)):
        self.position = position
        self.board = Board()
        self.moves = Tree(self.position)

    def calculate_moves(self, goal):
        '''Calculate the fewest moves to get to Goal position.  Goal is a tuple: (x,y)'''
        #check if already at goal, if so return 
        #check each move 
        # if goal return path to root
        #if not, for each move, calculate teh next step of moves 
        found = False
        count = 0
        goal_node = None
        visited = []
        q = queue.Queue()
        q.put(self.moves)
        while (not found) and count < 50: #prefent infinity
            #Dequeue and check
            item = q.get()
            visited.append(item.root)
            if item.root == goal:
                found = True
                goal_node = item
            else:
                #get it's submoves 
                move_array = self.move_function(item.root)
                f = filter(lambda move: False if move in visited else True, move_array)
                squares = list(f)
                for square in squares:
                    t = Tree(square)
                    item.add_branch(t)
                    q.put(t)

            count +=1
        return self.moves.return_path(goal)

            



    def add_moves(self, position):
        for move in self.move_function(position):
            self.moves.add_branch(move)

    def move_function(self, position):
        '''Output an array of potential moves for a KNIGHT'''
        end = []
        px, py = position
        #vertical then horizontal
        for move1 in [-2, 2]:
            for move2 in [-1, 1]:
                end.append((px + move2, py + move1))
        #horizontal then vertical
        for move1 in [-2, 2]:
            for move2 in [-1, 1]:
                end.append((px + move1, py + move2))
        
        return list(filter(self.board.on_board, end))
      

class Tree():
    def __init__(self, root):
        self.parent = None
        self.root = root
        self.branches = []

    def is_leaf(self):
        return self.branches == [] and isinstance(self, Tree)

    def subtrees(self):
        return self.branches

    def leaves(self):
        ''' Return the leaves of the tree'''
        if self.is_leaf():
            return self
        else:
            return [branch.leaves() for branch in self.branches]
    
    def add_branch(self, branch):
        if not isinstance(branch, Tree):
            branch = Tree(branch)
        self.branches.append(branch)
        branch.parent = self

    def find(self, value):
        '''Returns node with root of VALUE'''
        found = False
        count = 0
        goal_node = None
        q = queue.Queue()
        q.put(self)
        while (not found) and count < 50: #prefent infinity
            #Dequeue and check
            node = q.get()
            
            if node.root == value:
                found = True
                goal_node = node
            else:
                for b in node.branches:
                    q.put(b)
            count +=1
        return goal_node


    def return_path(self, value):
        #find the node
        node = self.find(value)
        #start path
        path = [node.root]
        current = node
        while current.parent is not None:
            current = current.parent
            path.append(current.root)
        path.reverse()
        return path

        
        
                
#Tests
k = Knight((3,3))
# k.add_moves(k.position)
# print(k.moves.leaves())
# print(k.moves.return_path((7,2)))
print(k.calculate_moves((0,0)))