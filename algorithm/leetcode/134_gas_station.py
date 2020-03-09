class Solution(object):
    def canCompleteCircuit(self, gas, cost):
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """
        max_pos = 0
        net, lnet = [], len(gas)
        for i in range(lnet):
            net.append(gas[i] - cost[i])
            if net[i] > net[max_pos]:
                max_pos = i
        _sum = net[max_pos]
        left, right = (max_pos-1)%lnet, (max_pos+1)%lnet
        while left != right:
            if net[left] > net[right]:
                _sum += net[left]
                left = (left-1)%lnet
            else:
                _sum += net[right]
                right = (right+1)%lnet
        return -1 if _sum+net[right] < 0 else (right+1)%lnet

if __name__ == '__main__':
    gas = [1, 2, 3, 4, 5]
    cost = [3, 4, 5, 1, 2]
    assert Solution().canCompleteCircuit(gas, cost) == 3

    gas = [2, 3, 4]
    cost = [3, 4, 3]
    assert Solution().canCompleteCircuit(gas, cost) == -1

    gas = [5, 1, 2, 3, 4]
    cost = [4, 4, 1, 5, 1]
    assert Solution().canCompleteCircuit(gas, cost) == 4
