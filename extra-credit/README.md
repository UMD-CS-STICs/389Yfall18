# Extra Credit
### Due: December 14th
For extra credit answer the following questions using the provided simulation (you can run the simulation with `python sim.py`)

## Questions (Written Response)
1. Define loop closure and give an example.
1. What happens to the quality of the solution to the SLAM problem when the car spawns far away from any observable landmarks and has to move to see the first one? Why does this happen? How could this behavior be fixed?
1. Observe the following map (where the green dots are landmarks and the red ellipses are covariances):  
![Imgur](https://i.imgur.com/mp3yCSr.png)  
How certain could the robot possibly be about its location if it used this map to localize? In other words, what is the lower bound for the covariance, and why?
1. Given sufficient time and under the correct conditions, KF SLAM will be equally certain about the locations of all landmarks. Given the map above, what is the lower bound on how certain each landmark can be?
1. Traditional SLAM algorithms are passive, meaning they just process the information the robot has available and don't influence the robot's motion decisions. Explain how an "active" SLAM algorithm, that influenced exploration decisions, could improve the time it would take the algorithm to obtain a reasonable estimate for all the landmarks.

## Submission
Please email me your responses
