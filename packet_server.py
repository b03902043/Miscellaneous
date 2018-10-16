
import time
import random
import numpy as np
from packet_client import PacketAssembler, PacketAssembler2

DEBUG = True

class PacketServer:

    def __init__(self, overlap=False, duplicate=False, multithread=False):
        self.clients = []
        self.done = False
        self.data = None
        self.prepared = False
        self.flags = {
            'overlap': overlap,
            'duplicate': duplicate,
            'multithread': multithread,
        }

    def setData(self, data):
        self.data = data
        self.prepared = False

    def _prepare(self, pieces=5):
        idx = np.append([0], np.sort(np.random.choice(range(1, len(self.data)-1), size=pieces-1, replace=False)))
        lengths = np.append(np.diff(idx), [len(self.data) - idx[-1]])
        self._data = [(_i, self.data[_i:][:l+(1 if self.flags['overlap'] else 0)]) for _i, l in zip(idx, lengths)]
        if self.flags['duplicate']:
            self._data *= 2 # duplicate test
        random.shuffle(self._data)
        self.pData = iter(self._data)
        self.prepared = True
        return self

    def register(self, client):
        self.clients.append(client)

    def dispatch(self):
        assert self.prepared, "{0}._prepare() not being called after {0}.setData()".format("PacketServer")
        try:
            pkt = next(self.pData)
            for c in self.clients:
                c.putPacket(*pkt)
        except StopIteration:
            self.done = True

    @property
    def alive(self):
        return not self.done

if __name__ == '__main__':
    serv = PacketServer(overlap=True)
    cli = PacketAssembler2()
    serv.register(cli)
    dat = '''昨夜風開露井桃，未央前殿月輪高。平陽歌舞新承寵，簾外春寒賜錦袍。'''
    serv.setData(dat)
    serv._prepare()
    while serv.alive:
        time.sleep(0.01)
        serv.dispatch()
        if DEBUG:
            cli.Print()
    print(cli.read(len(dat)))


