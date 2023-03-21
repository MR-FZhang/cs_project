
import random
candidates = ["B"]

candidate_a = []
candidate_b = []

stacks = ["A" for _ in range(100)]
for i in range(52):
    done = False
    while not done:
        rnd=random.randint(0,99)
        if stacks[rnd] == "A":
            stacks[rnd] = "B"
            done = True
count = 0
for i in range (len(stacks)-1):
  if stacks[i] == "A":
    count += 1
print (count)
print(stacks)
selection = False
for item in stacks:
  item = stacks.pop()
  if item == 'A':
    candidate_a.append(item)

  elif item == 'B':
    candidate_b.append(item)

for votes in candidate_a:
  vote_a = candidate_a.pop()
  vote_b = candidate_b.pop()
  if vote_b == -1 and selection == False:
    print('candidate_a has more votes')
    selection = True
  elif selection == False:
    print('candidate_b has more votes')
    selection = True