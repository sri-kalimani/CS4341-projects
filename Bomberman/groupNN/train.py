# Used to run variants multiple times for reinforcement learning

import variant1 as v1
import variant2 as v2
import variant3 as v3
import variant4 as v4
import variant5 as v5

# Number of times to run file
numtests = 250
randomMove = 0
randomMoveStep = -0.01

# Set all to training
v1.training = True
v2.training = True
v3.training = True
v4.training = True
v5.training = True

for i in range(numtests):

    v1.initialize(randomMove)
    v2.initialize(randomMove)
    v3.initialize(randomMove)
    v4.initialize(randomMove)
    v5.initialize(randomMove)
    
    # Increase or decrease randomMove by the step
    randomMove += randomMoveStep
