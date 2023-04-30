class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def update(self, index, value):
        while index <= self.size:
            self.tree[index] += value
            index += index & -index

    def prefix_sum(self, index):
        result = 0
        while index > 0:
            result += self.tree[index]
            index -= index & -index
        return result

    def find_median(self):
        total = self.prefix_sum(self.size)
        target = (total + 1) // 2
        index = 0
        cum_freq = 0
        while cum_freq < target:
            index += 1
            cum_freq = self.prefix_sum(index)
        return index
    
    def range_sum(self, left, right):
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    def delete(self, index, value):
        self.update(index, -value)

# def find_list_median(lst):
#     max_value = max(lst)
#     fenwick_tree = FenwickTree(max_value)

#     for num in lst:
#         fenwick_tree.update(num, 1)

#     return fenwick_tree.find_median()

# if __name__ == "__main__":
#     lst = [10, 6, 71, 8, 5, 1]
#     median = find_list_median(lst)
#     print("Median:", median)
