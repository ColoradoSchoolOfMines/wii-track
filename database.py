import socket

class BinTree:
    def __init__(self):
        self.root = None
        self.left = None
        self.right = None
    def add(self, new_elem):
        if self.root == None:
            self.root = new_elem
            self.left = BinTree()
            self.right = BinTree()
        else:
            if new_elem[0] < self.root[0]:
                self.left.add(new_elem)
            else:
                self.right.add(new_elem)
    def look_up(self, key):
        if self.left.root == None and self.right.root == None:
            return (self.root[1], (abs(key - self.root[0]) / key))
        elif self.root[0] == key:
            return (self.root[1], (abs(key - self.root[0]) / key))
        else:
            if key < self.root[0]:
                return self.left.look_up(key)
            else:
                return self.right.look_up(key)


def main():
    tree = BinTree()
    s = socket.socket()
    s.bind(('', 5000))
    s.listen()
    conn, addr = s.accept()
    while True:
        choice = input("Add new (n) or read (r)")
        data = float(conn.recv(1024))
        if choice == 'n':
            name = input("name")
            tree.add([data, name])
        else:
            print(tree.look_up(data))

if __name__ == "__main__":
    main()
