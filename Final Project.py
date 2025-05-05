import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import csv

x_coords = []
y_coords = []
distances = []
speeds = []

# webcam
capture = cv2.VideoCapture(0)

Focal = 450  # pixels
Real_Width = 10  # cm (real width of object, adjust as needed)

# Text font
font = cv2.FONT_HERSHEY_SIMPLEX
color = (255, 255, 255)

prev_time = time.time()
prev_center = None

while True:
    ret, img = capture.read()
    if not ret:
        break

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Blue color range
    lower_blue1 = np.array([90, 100, 70])
    upper_blue1 = np.array([110, 255, 255])
    lower_blue2 = np.array([111, 150, 70])
    upper_blue2 = np.array([130, 255, 255])

    # Masking
    mask1 = cv2.inRange(hsv_img, lower_blue1, upper_blue1)
    mask2 = cv2.inRange(hsv_img, lower_blue2, upper_blue2)
    mask = cv2.bitwise_or(mask1, mask2)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)

    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if contours:
        for c in contours:
            area = cv2.contourArea(c)
            if area > 500:
                x, y, w, h = cv2.boundingRect(c)
                center_x = x + w // 2
                center_y = y + h // 2
                curr_center = (center_x, center_y)

                perceived_width = w
                if perceived_width != 0:
                    distance = (Real_Width * Focal) / perceived_width  # in cm
                    x_coords.append(center_x)
                    y_coords.append(center_y)
                    distances.append(distance)

                    # Calculate speed
                    current_time = time.time()
                    if prev_center:
                        dx = curr_center[0] - prev_center[0]
                        dy = curr_center[1] - prev_center[1]
                        dist_pixels = (dx ** 2 + dy ** 2) ** 0.5

                        # Convert pixel movement to cm using perceived_width (scale)
                        pixels_per_cm = perceived_width / Real_Width
                        dist_cm = dist_pixels / pixels_per_cm
                        time_elapsed = current_time - prev_time
                        speed_cm_per_sec = dist_cm / time_elapsed
                        if speed_cm_per_sec > 6:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        else:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        speeds.append(speed_cm_per_sec)

                        cv2.putText(img, f"Speed: {speed_cm_per_sec:.2f} cm/s", (x, y + h + 60),
                                    font, 0.6, (0, 255, 255), 2)

                    prev_center = curr_center
                    prev_time = time.time()
                    cv2.circle(img, (center_x, center_y), 5, (0, 255, 0), -1)
                    cv2.putText(img, f"Center: ({center_x} X, {center_y}) Y", (x, y - 10),
                                font, 0.6, (0, 255, 0), 2)
                    cv2.putText(img, f"Distance: {distance:.2f} cm", (x, y + h + 30),
                                font, 0.6, color, 2)

                break  # Only largest object

    cv2.imshow("Blue Object Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

# Plots
plt.figure(figsize=(15, 5))

# 1. Path
plt.subplot(1, 3, 1)
plt.plot(x_coords, y_coords, marker='o')
plt.title("Object Path")
plt.xlabel("X (pixels)")
plt.ylabel("Y (pixels)")
plt.gca().invert_yaxis()
plt.grid(True)

# 2. Distance
plt.subplot(1, 3, 2)
plt.plot(distances, marker='x', color='blue')
plt.title("Distance Over Time")
plt.xlabel("Frame")
plt.ylabel("Distance (cm)")
plt.grid(True)
plt.tight_layout()
plt.show()


#CSV Data Storage
file = 'data_points.csv'
with open(file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["X", "Y", "Distance (cm)", "Speed (cm/s)"])
    for i in range(len(speeds)):
        writer.writerow([x_coords[i], y_coords[i], distances[i], speeds[i]])

print("Data saved to", file)
