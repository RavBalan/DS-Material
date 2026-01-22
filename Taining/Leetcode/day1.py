# Define the Solution class
class Solution:
    def __init__(self):
        pass
    
    def twoSum(self, nums, target):
        num_dict = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_dict:
                return [num_dict[complement], i]
            num_dict[num] = i
        return []

# Create an object
solver = Solution()

# Use the object to solve twoSum
nums = [2, 7, 11, 15]
target = 9
result = solver.twoSum(nums, target)
print(result)  # Output: [0, 1]

# Another test case
# nums = [3, 2, 4]
# target = 6
# result = solver.twoSum(nums, target)
# print(result)  # Output: [1, 2]
