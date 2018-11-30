# Project 2: Kalman Filters

## Introduction
In this project you will write a Kalman Filter for a 2D simulated environment. The simulation consists of a car moving to the right on a road, and pedestrinas trying to cross this road. Your Kalman Filter is important for self-driving cars, as it going to make sure we don't hit (or at least minimize the number of hits on) the pedestrians.

## Your Task
You need to write Kalman Filter to track the people crossing the road in a coordinate system with (0, 0) centered on the robot. Since we are only tracking the pedestrians relative to this refrence frame, there is no need to do localization on the car itself. All measurements are also given in this frame (so you don't have to worry about converting measurements to different reference frames). All of this work will be done in `kalmanfilter.py` file. Specifically, the tasks are the following.

### Step 1: Creating the Matrices
As you may remember from [this](https://docs.google.com/presentation/d/1mfR0dS5bIXp661stLHERnXHb6c4PR74f-lTraYiHHLM/edit?usp=sharing) lecture or the [codelab](https://github.com/UMD-CS-STICs/389Yfall18/tree/master/codelabs/05-nov2), there are a bunch of matrices we need to create before performing any operations. Specifically, we need the following matrices.

**A**: This is the state update transfomration matrix. Essentially, given our old state, what will our new state probably look like? This matrix should perform the operations required to get there. In this project, our state is going to be a 4x1 matrix with `pos_x`, `pos_y`, `vel_x`, and `vel_y`.

**B**: This is our control signal transformation matrix. As you may remember, this matrix takes in a control signal, and returns the vector (in the same shape as your state) that represents how the control signal changes your state. A control signal for this problem may be unintuitive, since we are tracking pedestrians, not a car, and we won't be able to get a "control signal" from the pedestrians. However, our car will accelerate to avoid hitting pedestrians, which will give the pedestrians an *apparent* acceleration in the opposite direction. Because of this you can use acceleration information from the car as a control signal for the pedestrians.

**C**: This is transformation matrix from your state space to the measurement space. Essentially, this matrix will convert a state into an expected measurement. We will be measuring x and y position.

While you also need matrices **R**, **Q**, and **I**, we are providing those to you. Lucky you! From the project directory, you can test this by running `python publictests.py`.

### Step 2 - 3: Prediction and Measurement Updates

In `kalmanfilter.py`, you will see the `prediction(control_signal)` and `measurement(measurements, Q)` functions that you need to fill in. You can find all instructions on what to do in `kalmanfilter.py`.

## Testing

For the public tests, you will need to run `python publictests.py`. For visual inspection, please run `python sim.py`. The red ovals/dots represent the states + covariances of all the people currently being tracked by the Kalman Filter.

## Questions for When You're Done
1. We could have tracked people with a histogram filter instead of a kalman filter. Talk about the pros and cons for each approach given this problem.
2. Remove all the code for the prediction update (replace it with a single line `pass` to avoid indentation issues) and re-run the Kalman Filter. What starts to happen? Why does this happen? Pay attention to the red circles + ovals that represent the covariances.
3. Spend some time thinking about the Q and R matrix, the covariances of the measurement and movement functions, respectively. While we just provide you these matrices here, how would you go about generating these matrices with a real self-driving car (you don't need to give a specific algorithm, just talk about the strategy in general)?

## Grading
Public Tests: 50%
Visual Inspection: 20%
Questions: 30%

## Submission
Please email me a `submission.zip` containing the entire contents of your `tracking/` directory along with a pdf, md file, or text file containing your answers to the questions. 
