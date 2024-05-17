import math
import os
import time
import numpy as np

# Define screen size
screen_size = 25

theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5
K1 = screen_size * K2 * 3 / (8 * (R1 + R2))

# Declare a function to render a frame
def render_frame(A: float, B: float):
    # Calculate the cos and sin values for A and B
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    # Define matrix for the output and z-buffer
    output = [[' ' for _ in range(screen_size)] for _ in range(screen_size)]
    zbuffer = [[0 for _ in range(screen_size)] for _ in range(screen_size)]

    # Iterate theta through an entire rotation
    theta = 0
    while theta < 2 * math.pi:
        # Define cos and sin of theta
        costheta = math.cos(theta)
        sintheta = math.sin(theta)
        
        # Iterate phi through an entire rotation
        phi = 0
        while phi < 2 * math.pi:
            # Define cos and sin of phi
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # Calculate x and y of the circle
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # Calculate x, y, z
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi - circley * cosA * sinB)
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi + circley * cosA * cosB)
            z = K2 + cosA * circlex * sinphi + circley * sinA

            ooz = 1 / z
            
            # Calculate the projection coordinates
            xp = int(screen_size / 2 + K1 * ooz * x)
            yp = int(screen_size / 2 - K1 * ooz * y)

            # Ensure the coordinates are within the screen bounds
            if 0 <= xp < screen_size and 0 <= yp < screen_size:
                # Calculate luminance
                L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

                # If L is bigger than 0, the surface is pointing towards the camera
                if L > 0:
                    if ooz > zbuffer[xp][yp]:
                        zbuffer[xp][yp] = ooz
                        luminance_index = int(L * 8)
                        luminance_index = min(luminance_index, len(".,-~:;=!*#$@") - 1)

                        output[xp][yp] = ".,-~:;=!*#$@"[luminance_index]
            phi += phi_spacing
        theta += theta_spacing

    # Print the frame
    print("\x1b[H")
    for j in range(screen_size):
        for i in range(screen_size):
            print(output[j][i], end="")
        print()

A = 1
B = 1
while True:
    render_frame(A, B)
    A += 0.07
    B += 0.03
    time.sleep(0.05)
    os.system("clear")