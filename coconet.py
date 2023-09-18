import matplotlib.pyplot as plt
import torch
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn_v2

# load the pre-trained model
model = maskrcnn_resnet50_fpn_v2(pretrained=True)

# put the model in evaluation mode
model.eval()

from PIL import Image, ImageStat

# load an image
image = Image.open("../bsc/bunny_hole/bunny15.jpg")
stat = ImageStat.Stat(image)
mean_r, mean_g, mean_b = [x/255.0 for x in stat.mean]
std_r, std_g, std_b = [x/255.0 for x in stat.stddev]
from torchvision.transforms import transforms

# define the image transformations
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0, 0, 0], [1, 1, 1])
])

# apply the transformations to the image
image_tensor = transform(image)
#print(image_tensor.shape)
#nomrimg = Image.fromarray(image_tensor.mul(255).byte().cpu().numpy())
#plt.imshow(image_tensor.permute(1,2,0))
#plt.show()
# run the model inference
with torch.no_grad():
    predictions = model([image_tensor])

# get the predicted masks
masks = predictions[0]['masks']
print(len(predictions[0]['masks']))
# convert the mask to a PIL image
mask = Image.fromarray(masks[7, 0].mul(255).byte().cpu().numpy())
#mask_Array=masks[0, 0].mul(255).byte().cpu().numpy()
#for i in range(len(masks)-1):
#    mask = Image.fromarray(masks[i, 0].mul(255).byte().cpu().numpy())
#    mask.show()
# show the mask
#mask = Image.fromarray(mask_Array)
mask.show()
