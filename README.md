# MFG-598-Abdirahman-Aden
# Final Project

## Required Imports:
1. cv2: For image processing and video capture (OpenCV)
2. numpy: For array and numerical operations
3. matplotlib.pyplot: To generate graphs
4. time: To measure time between frames and calculate speed
5. csv: To write the collected data into a spreadsheet

## Project Summary
This code uses a webcam to track a moving blue object in real time and calculate its position, distance, and speed. It does this by first capturing video frames and converting them to a format that makes it easier to detect colors (HSV). It looks specifically for shades of blue by using color filtering, called "masking," to isolate only the blue parts of the image. The program then identifies the largest blue object and calculates its distance from the camera using a formula that involves the known width of the object and the camera’s focal length. By comparing the object's position in each frame over time, it also calculates how fast the object is moving. This information is displayed on the screen, and a colored box is drawn around the object to indicate if it's moving fast (red) or slowly (blue). The user can stop the program at any time by pressing the 'q' key, which safely ends the video capture. Once stopped, the program generates visual graphs showing the object’s movement path and distance over time. It also saves all the collected data, including X and Y positions, distance, and speed, into a CSV file for further analysis and data collection.

## Project Video Link
[Project Video](https://drive.google.com/drive/u/0/folders/1fXV85g_dDkT8bKIKsPcQiLgXfSPaQIqH)
