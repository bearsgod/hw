RED = "red"
BLACK = "black"

class Stack:
    def __init__(self):
        self.items = []
    def push(self,item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def is_empty(self):
        return self.items == []

stk = Stack()

class Node:
    def __init__(self, newval):
        self.val = newval
        self.left = None
        self.right = None
        self.p = None
        self.bf = None
        self.color = None

class RBT:
    def __init__(self):
        self.nil = Node(None)
        self.root = self.nil

    def insert(self,n):
        y = self.nil
        x = self.root
        while x is not self.nil:
            y = x
            if n.val < x.val:
                x = x.left
            else: x = x.right
        n.p = y
        if y is self.nil:
            self.root = n
        elif n.val < y.val:
            y.left = n
        else: y.right = n
        n.left = self.nil
        n.right = self.nil
        n.color = RED
        self.insert_fixup(n)

    def insert_fixup(self,n):
        while n.p.color is RED:
            if n.p is n.p.p.left:
                y = n.p.p.right
                if y.color is RED:
                    n.p.color = BLACK
                    y.color = BLACK
                    n.p.p.color = RED
                    n = n.p.p
                else:
                    if n is n.p.right:
                        n = n.p
                        self.left_rotate(n)
                    n.p.color = BLACK
                    n.p.p.color = RED
                    self.right_rotate(n.p.p)
            else:
                y = n.p.p.left
                if y.color is RED:
                    n.p.color = BLACK
                    y.color = BLACK
                    n.p.p.color = RED
                    n = n.p.p
                else:
                    if n is n.p.left:
                        n = n.p
                        self.right_rotate(n)
                    n.p.color = BLACK
                    n.p.p.color = RED
                    self.left_rotate(n.p.p)
        self.root.color = BLACK

    def right_rotate(self,n):
        y = n.left
        n.left = y.right
        if y.right is not self.nil:
            y.right.p = n
        y.p = n.p
        if n.p is self.nil:
            self.root = y
        elif n is n.p.right:
            n.p.right = y
        else: n.p.left = y
        y.right = n
        n.p = y

    def left_rotate(self,n):
        y = n.right
        n.right = y.left
        if y.left is not self.nil:
            y.left.p = n
        y.p = n.p
        if n.p is self.nil:
            self.root = y
        elif n is n.p.left:
            n.p.left = y
        else: n.p.right = y
        y.left = n
        n.p = y

    def minimum(self,tree):
        while tree.left is not self.nil:
            tree = tree.left
        return tree

    def search(self, x, k):
        if None == x:
            x = self.root
        while x != self.nil and k != x.val:
            if k < x.val:
                x = x.left
            else:
                x = x.right
        return x

    def transplant(self,x,y):
        if x.p is self.nil:
            self.root = y
        elif x is x.p.left:
            x.p.left = y
        else: x.p.right = y
        if y is not self.nil:
            y.p = x.p

    def delete(self,z):
        y = z
        y_color = y.color
        if z.left is self.nil:
            x = z.right
            self.transplant(z,z.right)
        elif z.right is self.nil:
            x = z.left
            self.transplant(z,z.left)
        else:
            y = self.minimum(z.right)
            y_color = y.color
            x = y.right
            if y.p is z:
                x.p = y
            else:
                self.transplant(y,y.right)
                y.right = z.right
                y.right.p = y
            self.transplant(z,y)
            y.left = z.left
            y.left.p = y
            y.color = z.color
        if y_color is BLACK:
            self.delete_fixup(x)

    def delete_fixup(self,x):
        if x is self.nil:
            return
        while x is not self.root and x.color is BLACK:
            if x is x.p.left:
                w = x.p.right
                if w.color is RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.left_rotate(x.p)
                    w = x.p.right
                if w.left.color is BLACK and w.right.color is BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.right.color is BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.right_rotate(w)
                        w = x.p.right
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.right.color = BLACK
                    self.left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.color is RED:
                    w.color = BLACK
                    x.p.color = RED
                    self.right_rotate(x.p)
                    w = x.p.left
                if w.right.color is BLACK and w.left.color is BLACK:
                    w.color = RED
                    x = x.p
                else:
                    if w.left.color is BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.left_rotate(w)
                        w = x.p.left
                    w.color = x.p.color
                    x.p.color = BLACK
                    w.left.color = BLACK
                    self.right_rotate(x.p)
                    x = self.root
        x.color = BLACK

    def print(self,tree,level):
        if tree.right is not self.nil:
            self.print(tree.right,level + 1)
        for i in range(level):
            print('   ', end='')
        print(tree.val,tree.color)
        if tree.left is not self.nil:
            self.print(tree.left, level + 1)

    def get_bh(self,tree):
        if self is None:
            return
        else:
            bh = 0
            while tree is not self.nil:
                if tree.color is BLACK:
                    bh += 1
                tree = tree.right
            return bh

    def get_nb(self,tree):
        nb = 0
        while not stk.is_empty() or tree is not self.nil:
            if tree is not self.nil:
                stk.push(tree)
                tree = tree.left
            else:
                tree = stk.pop()
                if tree.color is BLACK:
                    nb += 1
                tree = tree.right
        return nb
        
    def inorder(self,tree):
        if self is None:
            return
        else:
            if tree.left is not self.nil:
                self.inorder(tree.left)
            print(tree.val)
            if tree.right is not self.nil:
                self.inorder(tree.right)

def main():
    rbt = RBT()
    f = open("input.txt", 'r')
    lines = f.readlines()
    check = 0

    total = 0
    
    for line in lines:
        n = int(line)
        if n > 0:
            In = Node(n)
            rbt.insert(In)
            total += 1
        elif n < 0:
            Out = abs(n)
            z = rbt.search(rbt.root,Out)
            if z is rbt.nil:
                print("There is no",Out)
            else:
                total -= 1
                rbt.delete(z)
        else: break

    print("\n")
    print("total =",total)
    print("nb =",rbt.get_nb(rbt.root))
    print("bh =",rbt.get_bh(rbt.root))
    print("\n")
    rbt.inorder(rbt.root)
    
    f.close()
    
main()
