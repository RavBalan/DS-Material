def search_element_in_array():
    import sys
    input = sys.stdin.read
    data = input().split()
    print(data)
    N = int(data[0])
    X = int(data[1])
    A = list(map(int, data[2:N+2]))  # Extracting array A
    
    if X in A:
        print("YES")
    else:
        print("NO")

# Call the function to execute
search_element_in_array()

# def findElement(A,X):
#     A_len = len(A)
#     output = []
#     for i in A:
#         for j in X:
#             if i == j:
#                output.append(1) 
    
#     if len(output) == A_len:
#         return 'YES'
#     else:
#         return 'NO'
                    
# A = [3, 10]
# X = [7, 3, 5, 2, 1]
# print(findElement(A, X))  # You expected "YES" but it prints "NO"
# def findElement(A, X):
#     return 'NO' if A in X else 'YES'

# A = [5, 3]
# X = [7, 3, 5, 2, 1]
# print(findElement(A, X))  # YES

# # X = 10
# # print(findElement(A, X))  # NO


