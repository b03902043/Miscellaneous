
# exchange rate converter
# data: [(A, B, 1.51), (B, C, 0.4)]
# input: A, C
# output: 6.04

from collections import deque

class ExchangeConverter:

    Impl = '''
        save relations in dict of lists pairwise ex.
        {   
            'TWD': [('NIO', 0.5) ...],
            'NIO': [('TWD', 2.0) ...],
        }

        BFS when converting
    '''

    def __init__(self):
        self.mapping = dict()

    def feed(self, data):
        for _from, _to, rate in data:
            self.mapping.setdefault(_from, []).append((_to, rate))
            self.mapping.setdefault(_to, []).append((_from, 1./rate))

    def convert(self, _from, _to):

        # Time: Omega(N)   --  N represents all currencies
        # Space: O(N)
        # TODO: this function can be optimized...

        bfs_q = deque([(_from, 1.)])
        bfs_bool = dict()
        while len(bfs_q) > 0:
            curr, rate = bfs_q.popleft()
            if curr == _to:
                return rate
            bfs_bool[curr] = True
            for _curr, _rate in self.mapping[curr]:
                if _curr not in bfs_bool:
                    bfs_q.append((_curr, rate*_rate))
        return None # find no relation between $_from and $_to

if __name__ == '__main__':
    data = [('TWD', 'USD', 0.03229), ('TWD', 'JPY', 3.6313), ('NIO', 'JPY', 3.4973)]
    machine = ExchangeConverter()
    machine.feed(data)

    print(machine.convert('NIO', 'NIO'))
    print(machine.convert('NIO', 'USD'))
    print(machine.convert('TWD', 'CNY'))
