import numpy as np

x = -0.639188
y = 0.075006
cos_phi = y/np.sqrt(x*x+y*y)
print(np.arccos(cos_phi)*180/np.pi + 181.21654376013205)

print(264.5237351690358 - 237.582)

# Sun position for all images from the set
# 90 - Altidute + 180
# Formula + azimuthal
# Worked better for the offset estimated camera than the actual camera
# 180.7761223820451 52.326023273332154