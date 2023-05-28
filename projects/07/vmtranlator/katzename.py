import random

namen = ['Sisso', 'Gigi', 'Gibuti', 'Swasti', 'Cesar', 'Eistafaista', 'Siesti', 'Katerchen', 'die Katze']

namen_anzahl = {name: 0 for name in namen}


for  _ in range(0,1000000):
  i = random.randint(0, len(namen)-1)
  namen_anzahl[namen[i]] += 1

max = 0
name = None

for n,a in namen_anzahl.items():
  if a > max:
    name = n
    max = a

print(namen_anzahl)
print("unser Kater heißt: '%s'" % name)