from torchvision import transforms
from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_V2_Weights,
    fasterrcnn_resnet50_fpn_v2,
)
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image

from PIL import Image

weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT

model = (
    fasterrcnn_resnet50_fpn_v2(
        weights=FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT,
        box_score_thresh=0.9,
    )
    .cuda()
    .eval()
)


img = Image.open("/root/learning-pytorch/data/voc/small-dataset/001001.jpg")

img = transforms.Compose([transforms.PILToTensor()])(img)
preprocess = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT.transforms()
batch = [preprocess(img).cuda()]

prediction = model(batch)[0]

labels = [weights.meta["categories"][i] for i in prediction["labels"]]
box = draw_bounding_boxes(
    img, boxes=prediction["boxes"], labels=labels, colors="red", width=4
)
im = to_pil_image(box.detach())
im.save("output.png")
