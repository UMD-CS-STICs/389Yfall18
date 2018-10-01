# Lane Line Fitting
![](https://i.imgur.com/ib49I1e.jpg)

In this project you will be fitting a polynomial model to each lane line on a road and then use those models to estimate the car's position on the road. You will complete the project in two parts. The first helps guide you through the process of building the pipeline on a single frame while the second applies your pipeline to an entire video. Both parts will be due Friday, September 28th at 11:59pm. You will submit the project by emailing me a zip file.

## Part One: Develop the Pipeline
Use the file `Pipeline Tester.ipynb` to develop your pipeline. I've outlined the general steps that your pipeline should include and wrote some visualization code that you might find helpful. However, you are in no way locked into the pipeline I have outlined. Feel free to modify the pipeline in any way you choose so long as the only libraries you use are numpy and opencv. Also feel free to ask for help writting visualization code in piazza if the code already provided is not sufficient to your needs. A completed part 1 should be a pipeline that takes a raw 3 channel image of a road, produces a polynomial model for each lane line, uses those models to estimate the car's position on the road (more information on this in the jupyter notebook), and visualizes the result (like in the image above).

## Part Two: Realtime Video and Write Up
Now that you have a working pipeline from part 1, in part 2 you will apply it to each sequence of a video. To do this you will edit `applied_pipeline.py`. You can run this file by executing `python applied_pipeline.py` in your terminal. I have placed `# TODO` in `applied_pipeline.py` to indicate where you can place your code. Here are some things to consider:
1. The yellow line in the video is harder to see that in the example picture, you might want to consider modifying your pipeline to use a different color space
1. You can just apply your pipeline to each frame of the video, but may get better performance if you use information from the previous frame to help build your model for the current frame.
1. Your pipeline should be fast enough to run in realtime, so make sure to replace for loops in your code with numpy functions wherever possible

In addition please provide a write up with your subission (either as a markdown file or a plaintext file) that answers these questions:
1. Describe your pipeline from part 1. What techniques did you find useful for each step?
1. Describe the changes you made to your pipeline for part 2. What difficulties did the video present?
1. What other techniques would you try to improve your pipeline's performance if you had more time?
