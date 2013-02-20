# each square is in a row, col, box (numbered 1-9 from L tor R then down)
# the Game instance has a list of rows, one of cols, and one of boxes
# each of the groupings in each list references the appropriate squares in
# their natural order
# I'd really like to do all the indices from 1, 
# but I'm not sure how and there's no internet here where I'm working on it

import sample

# this is for testing. Enter in game data here and it'll
# be added to the game
data = sample.veryhard1

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
    
    def rem(self, p):
        'remove possibility p from the list of possibilities'
        if p in self.poss:
            self.poss.remove(p)

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
        if type == "box":
            # these lists are the row and column numbers spanned by the box
            # these were interesting to figure out...
            # try this if you don't believe me:
            # for i in range(1,10):
            #     print i, [(i-1)/3*3 + n for n in [1,2,3]]
            self.rows = [(self.num-1)/3*3 + n for n in [1,2,3]]
            self.cols = [(self.num-1)%3*3 + n for n in [1,2,3]]
            # okay, I later realized that I probably won't need that
            # but I'm gonna keep it in there just 'coz
        self.squares = squares
        self.unsolved = squares[:] # make a copy
        self.needed = range(1,10)
        
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
        self.needed = []
        for n in range(1,10):
            if n not in found:
                self.needed.append(n)
        for sq in self.squares:
            if not sq.solved():
                old = sq.poss[:]
                for poss in found:
                    sq.rem(poss)
                if old != sq.poss:
                    same = False
        self.unsolved = []
        for sq in self.squares:
            if not sq.solved():
                self.unsolved.append(sq)
        return same
    
    def needs(self):
        '''checks a grouping to see if there's any number for which only
        one square can be that number (ie "this box needs a 6")'''
        self.check() # just to be sure we're dealing with updated info
        for n in range(1,10):
            poss_sqs = []
            for sq in self.squares:
                if n in sq.poss:
                    if sq.solved():
                        poss_sqs = [1,2,3]
                        # I know I should be able to save some calculations
                        # here by just skipping to the next number, but I'm
                        # not sure how to do that...
                    else:
                        poss_sqs.append(sq)
            if len(poss_sqs) == 1:
                # only one sq can be that number
                poss_sqs[0].poss = [n]

    def one_or_other(self):
        '''if there are n unsolved squares with identical possibilities
        of length n (ie two squares that are both either a 2 or a 3),
        remove all those possibilities from the remaining squares in that
        group'''
        self.check()
        remaining = []
        for sq in self.unsolved:
            remaining.append(sq.poss)
        for p in remaining:
            if len(p) == remaining.count(p):
                # 2 squares with the same 2 possibilities
                for sq in self.unsolved:
                    if sq.poss != p:
                        # remove those possibilities from sq
                        for possibility in p:
                            sq.rem(possibility)
    def in_line(self):
        '''This one is just for boxes.  If a box guarantees that a given 
        row or column has a 3 in it, then 3 must be removed from the 
        possibilities for the rest of the row or column'''
        self.check()
        if self.type != 'box':
            print "function 'in_line' is only for boxes"
            return
        for n in self.needed:
            rows = []
            cols = []
            for sq in self.unsolved:
                if n in sq.poss:
                    rows.append(sq.row)
                    cols.append(sq.col)
            if len(rows) == rows.count(rows[0]): # all the elements are the same
                return ('row', rows[0], n)
            elif len(cols) == cols.count(cols[0]):
                return ('col', cols[0], n)
            # note, this function only returns the row or col that needs to be
            # updated (or None), it doesn't actually update it
            
        
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
        
    def poss_remaining(self):
        rem = 0
        for square in self.squares:
            if not square.solved():
                rem += len(square.poss)
        return rem
                
    
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
        print "%d out of %d solved, %d possibilities remain" % (solved, tot, self.poss_remaining())
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
    
    def update(self, n=1, verbose=False):
        '''updates the possibilities of every row, col, and box, returns
        False if no changes were made'''
        same = True
        for i in range(n):
            for rcb in self.rows+self.cols+self.boxes:
                same = same and rcb.check()
            if verbose:
                g.show()
        return same
    
    def needs(self, n=1, verbose=False):
        '''checks every row, col, and box to see if they have only one 
        possibility for any given number'''
        for i in range(n):
            for rcb in self.rows+self.cols+self.boxes:
                rcb.needs()
            if verbose:
                g.show()
    
    def one_or_other(self, n=1, verbose=False):
        '''if there are n unsolved squares with identical possibilities
        of length n in a grouping (ie two squares that are both either a 2 or a 3),
        remove all those possibilities from the remaining squares in that
        group'''
        for i in range(n):
            for rcb in self.rows+self.cols+self.boxes:
                rcb.one_or_other()
            if verbose:
                g.show()
                
    def in_line(self, n=1, verbose=False):
        '''checks every box to see if they have a given number in a given
        row or column, then removes that number from the possibilities for
        the rest of the row or column'''
        for i in range(n):
            for box in self.boxes:
                a = box.in_line()
                if a:
                    if a[0] == "row":
                        # go through the squares in that row
                        for square in self.rows[a[1]-1].unsolved:
                            if square.col not in box.cols:
                            # oh shit, could I just do this?
                            # if square not in box.squares:
                                square.rem(a[2])
                    elif a[0] == "col":
                        for square in self.cols[a[1]-1].unsolved:
                            if square not in box.squares:
                                square.rem(a[2])
            if verbose:
                g.show()
    
    def master(self, n=1, verbose=False):
        '''cycles through the strategies the specified number of
        times'''
        for i in range(n):
            funcs = [self.needs, self.one_or_other, self.in_line]
            funcs[i%len(funcs)]()
            if verbose:
                g.show()

    def do_it(self):
        prev = 0
        while prev != self.poss_remaining():
            prev = self.poss_remaining()
            self.needs()
            self.one_or_other(),
            self.in_line()
            self.update()
        g.show()




g = Game()

for datum in data.strip().splitlines():
    g.add( int(datum[0]), int(datum[1]), int(datum[2]) )
g.show()

# to do: cp the rem method to old versions