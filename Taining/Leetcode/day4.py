class Solution:
    def hasDuplicate(self, nums: list[int]) -> bool:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                print(i,j)
                if nums[i] == nums[j]:
                    return True
        return False

Class = Solution()
print(Class.hasDuplicate([2,1,5,3,4]))