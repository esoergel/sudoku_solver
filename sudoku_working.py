# each square is in a row, col, box (numbered 1-9 from L tor R then down)
# the Game instance has a list of rows, one of cols, and one of boxes
# each of the groupings in each list references the appropriate squares in
# their natural order
# I'd really like to do all the indices from 1, 
# but I'm not sure how and there's no internet here where I'm working on it

# this iteration can remove possibilities solely by making sure that
# no row, col, or box has duplicates


class Square():
    def __init__(self, row=0, col=0, val=0):
        self.row = row
        self.col = col
        self.loc = (self.row, self.col)
        self.boxr = (self.row+2)/3
        self.boxc = (self.col+2)/3
        self.box = (self.boxr-1)*3 + self.boxc
        
        # boxp is position within the box, the line looks confusing, but it works
        self.boxp = ((self.row-1)%3)*3 + (self.col-1)%3+1
        if val:
            self.poss = [val]
        else:
            self.poss = range(1, 10)
    
    def solved(self):
        # boolean
        if len(self.poss) > 1:
            return False
        ## print "square", self.loc, self.poss
        self.val = self.poss[0]
        return True


class RCB():
    '''grouping for 9 squares, can be row, column, or box.
    the logic is the same for all 3.
    DO NOT try to iterate over a grouping,
    instead, use grouping.squares'''
    
    def __init__(self, type, num, squares):
        '''type="row"/"col"/"box", num=1-9
        squares is a list of 9 square objects'''
        self.type = type
        self.num = num
        self.squares = squares
        
        # sanity check
        if len(squares) > 9:
            print "ERROR! MORE THAN 9 SQUARES"

    def show(self):
        print "%s #%d" % (self.type, self.num)
        num = 1
        for sq in self.squares:
            print num, sq.poss
            num += 1
    
    def check(self):
        '''checks a grouping and removes (im)possibilities.
        It will also find duplicates and report the error'''
        found = []
        same = True # records whether or not a change was made
        for sq in self.squares:
            if sq.solved():
                if sq.val in found:
                    print "ERROR! There are two or more %d's in %s #%d" % (sq.val, self.type, self.num)
                    raise
                found.append(sq.val)
        for sq in self.squares:
            if not sq.solved():
                newposs = []
                for poss in sq.poss:
                    if poss not in found+newposs:
                        newposs.append(poss)
                if sq.poss != newposs:
                    same = False
                sq.poss = newposs
        return same
            

a = range(1, 10)
r = RCB("row", 1, a)

class Game():
    '''master class that stores a grouping of all the squares in a list,
    and all the rows, columns and boxes'''
    
    def __init__(self):
        self.squares = []
        for row in range(1, 10):
            for col in range(1, 10):
                a = Square(row, col, 0)
                self.squares.append(a)
                
        # initialize lists of all the rows, cols, and boxes
        # note that the indices will be from 0-8, 
        # I didn't feel like trying to fix that
        self.rows = [RCB('row', i, range(9)) for i in range(1, 10)]
        self.cols = [RCB('col', i, range(9)) for i in range(1, 10)]
        self.boxes = [RCB('box', i, range(9)) for i in range(1, 10)]
        
        for sq in self.squares:
            # populate rows, cols, and boxes
            r, c = sq.loc
            self.rows[r-1].squares[c-1] = sq
            self.cols[c-1].squares[r-1] = sq
            self.boxes[sq.box-1].squares[sq.boxp-1] = sq

            
    def add(self, row, col, val):
        '''updates the existing square at that location so it works elsewhere.
        do this rather than make a new square instance'''
        num = (row-1)*9 + col -1
        self.squares[num].poss = [val]
    
    def show(self):
        print ''
        solved = 0
        tot = 0
        for rnum, row in enumerate(self.rows):
            line = ""
            for square in row.squares:
                tot += 1
                if square.solved():
                    solved += 1
                    line += ' ' + str(square.val)
                else:
                    line += ' ' + '0'
            print line[:6] + ' |' + line[6:12] + ' |' + line[12:]
            if rnum in [2, 5]:
                print '-'*22
        print solved, "out of", tot, "solved"
        print ''
    
    def prompt(self, verbose=False):
        '''fast way to enter in data in terminal.  
        Use verbose to display the board each time'''
        go = True
        while go:
            raw = raw_input("enter row, col, and val in the format rcv\n")
            if not raw:
                go = False
            elif len(raw) != 3:
                print "try again"
            else:
                self.add( int(raw[0]), int(raw[1]), int(raw[2]) )
                if verbose:
                    g.show()
    
    def update(self, n=1):
        'updates the possibilities of every row, col, and box'
        for i in range(n):
            for rcb in self.rows+self.cols+self.boxes:
                rcb.check()




g = Game()

# this is for testing. Enter in game data here and it'll
# be added to the game
data = '''
118
132
151
169
194
227
233
264
314
329
331
347
419
455
488
549
567
621
653
697
763
772
781
795
845
878
883
915
941
959
974
996
'''
for datum in data.strip().splitlines():
    g.add( int(datum[0]), int(datum[1]), int(datum[2]) )
g.show()

