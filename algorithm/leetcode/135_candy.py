class Solution(object):
    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """
        last_peak, N = 0, len(ratings)
        candies = [1]
        for i in range(1, N):
            if ratings[i] > ratings[i-1]:
                last_peak = i
                candies.append(candies[i-1]+1)
            elif ratings[i] == ratings[i-1]:
                last_peak = i
                candies.append(1)
            else:
                candies.append(candies[i-1]-1)
                # check if reach valley
                if (i == N-1 or ratings[i] <= ratings[i+1]) and candies[i] != 1:
                    if candies[i] > 1:
                        delta = candies[i] - 1
                        for j in range(last_peak+1, i+1):
                            candies[j] -= delta
                    else: # candies[i] < 1
                        addi = 1 - candies[i]
                        for j in range(last_peak, i+1):
                            candies[j] += addi
        #print(candies)
        return sum(candies)

if __name__ == '__main__':
    ratings = [[1, 0, 2], [1, 2, 1], [1, 2, 3, 3, 3, 2, 1], [1, 3, 4, 5, 2]]
    for rat in ratings:
        print(Solution().candy(rat))
