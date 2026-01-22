import sys

# input = sys.stdin.read().split()
# input = map(int,input)
# input = [1,3,1,8,9,3,2]

# for i in input:
#     output = []          
#     if len(output) != 1:
#         for j in input:
#             if i > j:
#                 continue
#             else:                
#                 output.append(i)
#     output = list(set(output))
#     if len(output) == 1:
#         print(output)
    
# input = [1, 3, 1, 8, 9, 3, 19, 2]

# max_value = input[0]  # Start with the first element
# for i in input:
#     if i > max_value:
#         max_value = i

# print(max_value)  # Output: 9
    
    
    
# T = int(input())  # Number of test cases
# for _ in range(T):
#     N = int(input())  # Number of mountains
#     print(N,'M')
#     heights = list(map(int, input().split()))  # Heights of mountains

#     max_height = heights[0]  # Initialize max with the first element
#     for i in range(1, N):
#         if heights[i] > max_height:
#             max_height = heights[i]
    
#     print(max_height)
   


input = sys.stdin.read().split()
input = list(map(int, input))

index = 0
T = input[index]
index += 1

for _ in range(T):
    N = input[index]
    index += 1

    heights = input[index:index + N]
    index += N

    max_height = heights[0]
    for i in range(1, N):
        if heights[i] > max_height:
            max_height = heights[i]
    
    print(max_height)

