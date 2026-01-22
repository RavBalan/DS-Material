class Solution(object):
    def addTwoNumbers(self, l1, l2):
        result = []
        carry = 0
        i, j = 0, 0

        while i < len(l1) or j < len(l2) or carry:
            val1 = l1[i] if i < len(l1) else 0
            val2 = l2[j] if j < len(l2) else 0

            total = val1 + val2 + carry
            carry = total // 10
            result.append(total % 10)

            i += 1
            j += 1

        return result

sol = Solution()
output = sol.addTwoNumbers([2, 4, 3], [5, 6, 4])
print(output)  