import bpy
import numpy as np
import mathutils

# Set the output path for the reference image
reference_path = "/home/roneetnagale/DTU_OneDrive/DTU/bsc/blender_optim/11/ref.png"
rendered_path = "/home/roneetnagale/DTU_OneDrive/DTU/bsc/blender_optim/11/rendered.png"

# load the blender file
bpy.ops.wm.open_mainfile(filepath="/home/roneetnagale/Pictures/3D/Sun_optimization.blend")

bpy.context.scene.use_nodes = True
# Render the scene
#bpy.ops.render.render(write_still=True)

# Save the reference image
#bpy.data.images['Render Result'].save_render(reference_path)

learning_rate = 0.005
beta1 = 0.9
beta2 = 0.999
epsilon = 1e-8

m = 0  # Exponential moving average of gradient
v = 0  # Exponential moving average of squared gradient
t = 0  # Time ste

def adam_update_step(gradient):
    global m, v, t

    t += 1
    m = beta1 * m + (1 - beta1) * gradient
    v = beta2 * v + (1 - beta2) * (gradient ** 2)

    m_hat = m / (1 - beta1 ** t)
    v_hat = v / (1 - beta2 ** t)

    update = learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)

    return update


def calculate_loss(rotation, rendered_path = rendered_path, reference_path=reference_path):

    set_light_rotation(rotation)

    #render image
    bpy.ops.render.render(write_still=True)
    # Load the rendered image

    bpy.data.images['Render Result'].save_render(rendered_path)
    rendered_image = bpy.data.images.load(rendered_path).pixels[:]

    # Load the reference image
    reference_image = bpy.data.images.load(reference_path).pixels[:]

    # calculate loss
    diff = np.array(rendered_image) - np.array(reference_image)
    mse = np.mean(diff**2)
    return -mse

def set_light_rotation(rotation):
    sun_light = bpy.data.objects['Sun']
    print(rotation)
    sun_light.rotation_euler = rotation


def calculate_gradient(metric_func, rotation, epsilon=0.005):
#    gradients = []

    perturbation = [0.0, 0.0, 0.0]
    perturbation[2] = epsilon
    #perturbation = mathutils.Euler(perturbation, "XYZ")
    metric_plus = metric_func(np.add(list(rotation),perturbation))
    metric_minus = metric_func(np.subtract(list(rotation), perturbation))

    gradient = (metric_plus - metric_minus) / (2.0 * epsilon)
    #gradients.append(gradient)

    return gradient

# Set the learning rate and number of iterations
num_iterations = 100

for iteration in range(num_iterations):
    # Render the scene with the current light position

    current_rotation = bpy.data.objects['Sun'].rotation_euler

    gradient = calculate_gradient(calculate_loss,current_rotation)

    update = adam_update_step(gradient)



    rotation = bpy.data.objects['Sun'].rotation_euler
    rotation[2] += update  # Update Z rotation only
    bpy.data.objects['Sun'].rotation_euler = rotation
    print(rotation)
    loss = calculate_loss(rotation,rendered_path, reference_path)
    # print(rendered_image)

    # Load the reference image<


    # Calculate the loss

    print(f"Iteration: {iteration+1}, Loss: {loss}")

# Render the final optimized scene
bpy.ops.render.render(write_still=True)


""" lit009 sun <Euler (x=3.7991, y=0.0000, z=4.1389), order='XYZ'>
<Euler (x=3.7991, y=0.0000, z=4.1389), order='XYZ'> """
