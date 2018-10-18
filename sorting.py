
import sys
import time
import unittest
import numpy as np

def printf(_str):
    sys.stdout.write(_str)
    sys.stdout.flush()

class SortChecker(unittest.TestCase):

    MAX_TIMES = 10

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        printf('%.3f ' % t)

    def base_sort(self, cls):
        np.random.seed(6)
        for _ in range(self.MAX_TIMES):
            with self.subTest(iteration=_):
                #ar = np.random.randint(1, 100, 1000)
                ar = np.random.random(1000)
                answer = np.sort(ar)
                result = cls(ar).run()
                self.assertTrue(np.all(result == answer))

    def test_heapsort(self):
        self.base_sort(HeapSort)
    def test_mergesort(self):
        self.base_sort(MergeSort)
    def test_quicksort(self):
        self.base_sort(QuickSort)

class MergeSort:

    Time = 'O(NlogN)'
    Space = 'O(N)'

    def __init__(self, array):
        self.array = array
        self.tmp = [0]*len(array)

    def run(self):
        return self.merge_sort(self.array, 0, len(self.array))
        
    def merge_sort(self, array, start, end):
        if end - start < 2:
            return
        self.merge_sort(array, start, (start+end)//2)
        self.merge_sort(array, (start+end)//2, end)
        self.merge(array, start, end)
        return self.array

    def merge(self, array, start, end):
        middle = (start+end)//2
        s1, s2 = start, middle
        index = start
        while s1 < middle and s2 < end:
            if array[s1] < array[s2]:
                self.tmp[index] = array[s1]
                s1 += 1
            else:
                self.tmp[index] = array[s2]
                s2 += 1
            index += 1
        for i in range(s1, middle):
            self.tmp[index] = array[i]
            index += 1
        for i in range(s2, end):
            self.tmp[index] = array[i]
            index += 1

        array[start:end] = self.tmp[start:end]

class HeapSort:

    Impl = ''' 
    1. create max_heap
    2. pop root, then re-heapify max_heap
        root
       /    \
     left  right
    left = 2*root + 1
    right = 2*root + 2
    '''
    Time = 'O(NlogN)'
    Space = 'O(1)'

    def __init__(self, array):
        self.array = array

    def run(self):
        N = len(self.array)
        # create max heap ( process node from large index to small
        for i in range(N//2 - 1, -1, -1):
            self.heapify(self.array, N, i)
        # tidy up element one-by-one
        for i in range(N-1, -1, -1):
            self.array[0], self.array[i] = self.array[i], self.array[0]
            self.heapify(self.array, i, 0)

        return self.array

    def heapify(self, array, N, idx):
        # @N: max length processed of array
        # @idx: current element index in max_heap
        left, right, largest = 2*idx+1, 2*idx+2, idx
        if left < N and array[left] > array[largest]:
            largest = left
        if right < N and array[right] > array[largest]:
            largest = right
        #v1 = None if left >= N else array[left]
        #v2 = None if right >= N else array[right]
        if largest != idx:
            array[idx], array[largest] = array[largest], array[idx]
            self.heapify(array, N, largest)

class QuickSort:

    Time = 'O(NlogN) ~ O(N^2)'
    Space = 'O(1)'

    def __init__(self, array):
        self.array = array

    def run(self):
        return self.qsort(self.array, 0, len(self.array))

    def qsort(self, array, start, end):
        if end - start <= 1:
            return
        # find pivot, put elements smaller than it to left, otherwise right
        ptr, o_pIdx = start, (start+end)//2
        pivot = array[o_pIdx]
        array[o_pIdx], array[end-1] = array[end-1], array[o_pIdx]
        for i in range(start, end-1):
            if array[i] < pivot:
                array[i], array[ptr] = array[ptr], array[i]
                ptr += 1
        array[ptr], array[end-1] = array[end-1], array[ptr]

        # sort left & right part (ptr denotes that index of pivot)
        self.qsort(array, start, ptr)
        self.qsort(array, ptr+1, end)
        return array


if __name__ == '__main__':
    unittest.main(verbosity=2)

