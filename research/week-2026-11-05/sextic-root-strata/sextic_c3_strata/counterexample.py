from explore import gate
H={(4,2):1,(6,0):1};G={(1,1):1}
for j in range(4):
 print(j,G,'T3',gate(H,G,3),'T5',gate(H,G,5))
 G=gate(H,G,1)
