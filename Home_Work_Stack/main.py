class Stack:
    def __init__(self):
        self.values = list()

    def is_empty(self):
        return not self.size()

    def size(self):
        return len(self.values)

    def push(self, item):
        self.values.append(item)

    def pop(self):
        return self.values.pop(-1)

    def peek(self):
        return self.values[-1]

    def check_in(self, item):
        return item in self.values


def is_balanced(value: str):
    closed = Stack()
    for i in value:
        i = ord(i)
        if not closed.is_empty():
            if closed.peek() == i or closed.peek() + 1 == i:
                closed.pop()
                continue
            elif closed.check_in(i):
                return False
        closed.push(i + 1)
    return closed.is_empty()


def print_balanced():
    print('Сбалансированно' if is_balanced(input())
            else 'Несбалансированно')


if __name__ == '__main__':
    print_balanced()




