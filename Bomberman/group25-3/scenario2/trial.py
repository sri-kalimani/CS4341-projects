# Used to run variants multiple times for reinforcement learning

import variant1 as v1
import variant2 as v2
import variant3 as v3
import variant4 as v4
import variant5 as v5

# Number of times to run file
numtests = 10

cv1 = 0
cv2 = 0
cv3 = 0
cv4 = 0
cv5 = 0

for i in range(numtests):

    cv1 += 1 if v1.initialize(0) else 0
    cv2 += 1 if v2.initialize(0) else 0
    cv3 += 1 if v3.initialize(0) else 0
    cv4 += 1 if v4.initialize(0) else 0
    cv5 += 1 if v5.initialize(0) else 0
    
print("v1: " + str(cv1) + "/" + str(numtests))
print("v2: " + str(cv2) + "/" + str(numtests))
print("v3: " + str(cv3) + "/" + str(numtests))
print("v4: " + str(cv4) + "/" + str(numtests))
print("v5: " + str(cv5) + "/" + str(numtests))