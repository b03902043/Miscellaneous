
# 1. chunks that donot overlap each other  ->  done
# 2. can overlap
# 3. threading

class PacketAssembler:

    def __init__(self):
        self.ptr, self.offset = 0, 0
        self.pdict = dict()

    def putPacket(self, offset, data):
        # @offset: int
        # @data: str
        if offset in self.pdict or offset < self.ptr:
            print('drop duplicate')
            return 
        print('Receive (%d, "%s")' % (offset, data))
        self.pdict[offset] = data

    def read(self, maxlen):
        # @maxlen: int
        data = ''
        upper = maxlen
        while self.ptr in self.pdict and upper > 0:
            _dat = self.pdict[self.ptr]
            if len(_dat) > upper:
                data += _dat[:upper]
                self.pdict[self.ptr + upper] = self.pdict[self.ptr][upper:]
                del self.pdict[self.ptr]
                self.ptr += upper
                break
            data += _dat
            self.ptr += len(_dat)
            upper -= len(_dat)
        return data

    def Print(self):
        print(', '.join([ '[%d, %d)' % (off, off+len(dat)) for off, dat in self.pdict.items()]))

'''
Interval Linked List
'''
class IntervalNode:

    def __init__(self, start, data):
        self.start = start
        self.end = start + len(data)
        self.data = data
        self.parent = None
        self.next = None

    def toList(self):
        _next, result = self.next, [self]
        while _next is not None:
            result.append(_next)
            _next = _next.next
        return result

class PacketAssembler2:

    Impl = 'IntervalLinkedList'
    EMPTY = ''

    def __init__(self):
        self.ptr = 0
        self.head = None
        self.tail = None

    def putPacket(self, offset, data):
        node = IntervalNode(offset, data)
        print('Receive (%d, "%s")' % (offset, data))
        if node.end <= self.ptr:
            return
        elif node.start < self.ptr:
            node.start = self.ptr
            node.data = node.data[self.ptr-node.start:]
        #print(node.start, node.end)

        if self.head is None:
            self.head = self.tail = node
            return

        ctr, _node = 0, self.head
        ctr_s, ctr_e = -1, -1
        node_s, node_e = None, None
        while _node is not None:
            if ctr_s == -1:
                if node.start < _node.start:  # equal sign dont care
                    ctr_s = ctr
                    node_s = _node
                elif node.start <= _node.end:
                    ctr_s = ctr + 1
                    node_s = _node
            
            if ctr_s != -1 and ctr_e == -1: # after determined ctr_s
                if node.end < _node.start:
                    ctr_e = ctr
                    node_e = _node
                elif node.end < _node.end:  # equal sign dont care
                    ctr_e = ctr + 1
                    node_e = _node
            _node = _node.next
            ctr += 2
        if node_s is None:
            o_tail, self.tail = self.tail, node
            o_tail.next = self.tail
            self.tail.parent = o_tail
            return
        elif node_e is None:
            self.tail.data += node.data[self.tail.end - node.start:]
            self.tail.end = node.end # extend last first
            node_e = self.tail
            ctr_e = ctr-1 # last [s, e) part

        #print(node.start, node.end, ctr_s, ctr_e)
        # - : ctr_s % 2 == 1
        # + : ctr_s % 2 == 0
        if ctr_s == ctr_e:
            if ctr_s % 2 == 0:
                node.parent = node_s.parent
                if self.head is not node_s:
                    node.parent.next = node
                else:
                    self.head = node
                node_s.parent = node
                node.next = node_s
        else:
            same_sign = (ctr_s + ctr_e) % 2 == 0
            first_is_plus = ctr_s % 2 == 0
            #print(same_sign, first_is_plus, ctr_s, ctr_e)
            #print(node_s.start, node_e.start)
            if same_sign and first_is_plus: # ++
                node.parent = node_s.parent
                node.next = node_e
                if node.parent is None:
                    self.head = node
                # free up nodes between [node_s, node_e)
                while node_s != node_e:
                    del node_s.data
                    node_s = node_s.next
            elif same_sign: # --
                # merge into node_s
                node_s.next = node_e.next
                node_s.data = '%s%s%s' % (node_s.data, node.data[node_s.end - node.start: node_e.start - node.start], node_e.data)
                node_s.end = node_e.end
                if self.tail is node_e:
                    self.tail = node_s
            elif first_is_plus: # +-
                # merge into node_e
                node_e.parent = node_s.parent
                node_e.data = '%s%s' % (node.data, node_e.data[node.end-node_e.start:])
                node_e.start = node.start
                if node_e.parent is None:
                    self.head = node_e
                else:
                    node_e.parent.next = node_e
            else: # -+
                # merge into node_s
                node_s.end = node.end
                node_s.next = node_e
                node_s.data = '%s%s' % (node_s.data[:node.start-node_s.start], node.data)
                node_e.parent = node_s

    def read(self, maxlen):
        if self.head is None or maxlen == 0 or self.ptr != self.head.start:
            return self.EMPTY

        dat = self.head.data[:maxlen]
        if self.head.end - self.head.start > maxlen:
            self.ptr = self.head.start = self.head.start + maxlen
            self.head.data = self.head.data[maxlen:]
        else:
            self.ptr = self.head.end
            self.head = self.head.next
        return dat

    def Print(self):
        if self.head is None:
            print(self.EMPTY)
            return

        print(' -> '.join([ '[%d, %d) |%s| ' % (ptr.start, ptr.end, ptr.data) for ptr in self.head.toList() ]))

