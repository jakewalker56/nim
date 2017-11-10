# rows dimension definition:
# 0 - how many remaining rows
# 1 - row 1 value
# 2 - row 2 value
# ...

maxrowsize = 7
maxrows = 4
globalrowindex = 0

def create_nested_layers(rows, rowsize):
  if rows == 1:
    result = []
    for i in range(rowsize):
      result.append([0,0,0])
    return result
  else:
    result = []
    for i in range(rowsize):
      result.append(create_nested_layers(rows-1, rowsize))
    return result

def create_nesting(rows, rowsize):
  result = []
  for i in range(rows):
    result.append(create_nested_layers(i+1, rowsize))
  return result

def set_state_value(subgraph, positions, val):
  if isinstance(positions, int) == 1:
    subgraph[position] = val
  elif len(positions) == 1:
    subgraph[positions[0]] = val
  else:
    set_state_value(subgraph[positions[0]], positions[1:], val)

def get_state_value(subgraph, positions):
  if isinstance(positions, int) == 1:
    return subgraph[positions]
  elif len(positions) == 1:
    return subgraph[positions[0]]
  else:
    return get_state_value(subgraph[positions[0]], positions[1:])

def explore_subgraph(subgraph, positions, depth):
  global rows
  if isinstance(subgraph, int):
    #should always be an arrao of 3 values
    return
  if ((1 if isinstance(positions, int) else len(positions)) == depth):
    #this is the terminating depth
    if subgraph[0] == 0:
      #we have to go through all the possible changes until we find an answer
      for i in range(len(positions)):
        #pick the row to modify
        for k in range(positions[i]):
          #pick how much to leave
          tmp = positions[:]
          tmp[i] = k
          if get_state_value(rows[globalrowindex], tmp)[0] == -1:
            #we put the enemy in a position to lose
            set_state_value(rows[globalrowindex], positions, [1, i, k])
            return
        #now try deleting the row
        tmp = positions[:]
        del tmp[i]
        if get_state_value(rows[depth - 2], tmp)[0] ==-1:
          set_state_value(rows[globalrowindex], positions, [1, i, -1])
          return
      #there is no move to win, therefore any move will make you lose; make a random move
      set_state_value(rows[globalrowindex], positions, [-1, 0, 0])
  else:
    for i in range(len(subgraph)):
      tmp = positions[:]
      tmp.append(i)
      explore_subgraph(subgraph[i], tmp, depth)

#create dynamic programming array  
rows=create_nesting(maxrows, maxrowsize)
  
#initialize
rows[0][0] = [-1, 0, 0]

#fill out dynamic programming array
for i in range(maxrows):
  globalrowindex = i
  explore_subgraph(rows[globalrowindex], [], globalrowindex + 1)

# result triplet:
#  0 - +1 indicates win, -1 indicates loss, 0 indicates unknown
#  1 - indicates which row to act on to acheive result (row index starts at 0)
#  2 - indicates how many tokens to leave in that row (-1 means delete)(add one to convert from index to actual number of tokens)

print("example 2 remaining rows of 1 and 1 (expected = [1, 0, -1]")
print(rows[1][0][0])

print("example 2 remaining rows of 1 and 2 (expected = [1, 0, -1]")
print(rows[1][0][1])

print("example 2 remaining rows of 2 and 2 (expected = [-1, 0, 0]")
print(rows[1][1][1])

print("example 3 remaining rows of 1, 1 and 1 (expected = [-1, 0, 0]")
print(rows[2][0][0][0])

print("example 3 remaining rows of 2, 1 and 1 (expected = [1, 0, 0]")
print(rows[2][1][0][0])

print("example 3 remaining rows of 1, 2 and 1 (expected = [1, 1, 0]")
print(rows[2][0][1][0])

print("TEST: 4 rows of 1, 3, 5, 7")
print(rows[3][0][2][4][6])

#print("TEST: 3 rows of 3, 5, 7")
#print(rows[2][2][4][6])

print("TEST: 4 rows of 1, 3, 4, 7")
print(rows[3][0][2][3][6])

print("TEST: 3 rows of 2, 4, 7")
print(rows[2][1][3][6])

print("TEST: 3 rows of 1, 4, 6")
print(rows[2][0][3][5])

print("TEST: 2 rows of 4, 5")
print(rows[1][3][4])

print("TEST: 2 rows of 3, 4")
print(rows[1][2][3])
