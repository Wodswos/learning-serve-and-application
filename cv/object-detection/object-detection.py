import numpy as np
import torch
from ray.data import Dataset
from torchvision import transforms
from torchvision.models.detection import (
    FasterRCNN_ResNet50_FPN_V2_Weights,
    fasterrcnn_resnet50_fpn_v2,
)
from typing import Dict
import uuid

import ray
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
from torchvision.transforms.functional import convert_image_dtype, to_tensor


def preprocess_image(data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    preprocessor = transforms.Compose(
        [transforms.ToTensor(), weights.transforms()]
    )
    return {
        "image": data["image"],
        "transformed": preprocessor(data["image"]),
    }


class ObjectDetectionModel:
    def __init__(self):
        # Define the model loading and initialization code in `__init__`.
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        self.model = fasterrcnn_resnet50_fpn_v2(
            weights=self.weights,
            box_score_thresh=0.9,
        )
        if torch.cuda.is_available():
            # Move the model to GPU if it's available.
            self.model = self.model.cuda()
        self.model.eval()

    def __call__(self, input_batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        # Define the per-batch inference code in `__call__`.
        batch = [torch.from_numpy(image) for image in input_batch["transformed"]]
        if torch.cuda.is_available():
            # Move the data to GPU if it's available.
            batch = [image.cuda() for image in batch]
        predictions = self.model(batch)
        return {
            "image": input_batch["image"],
            "labels": [
                pred["labels"].detach().cpu().numpy() for pred in predictions
            ],
            "boxes": [
                pred["boxes"].detach().cpu().numpy() for pred in predictions
            ],
        }


ds: Dataset = ray.data.read_images("/root/learning-pytorch/data/voc/small-dataset")

ds = ds.map(preprocess_image)
ds = ds.map_batches(
    ObjectDetectionModel,
    concurrency=1,
    batch_size=2,  # Use the largest batch size that can fit in GPU memory.
    # Specify 1 GPU per model replica.
    num_gpus=1,
)

# batch = ds.take_batch(batch_size=2)
for batch in ds.iter_batches():
    for image, labels, boxes in zip(batch["image"], batch["labels"], batch["boxes"]):
        image = convert_image_dtype(to_tensor(image), torch.uint8)
        labels = [
            FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT.meta["categories"][i]
            for i in labels
        ]
        boxes = torch.from_numpy(boxes)
        img = to_pil_image(
            draw_bounding_boxes(
                image,
                boxes,
                labels=labels,
                colors="red",
                width=4,
            )
        )
        # display(img)

        img.save(
            f"/root/learning-pytorch/data/voc/small-dataset-output/image_{uuid.uuid4()}.png"
        )
