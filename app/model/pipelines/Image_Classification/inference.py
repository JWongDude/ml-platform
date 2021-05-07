# inference.py 
# Image Classification Inference 
from pathlib import Path
from PIL import Image
import torch                                # For tensor manipulation
from torchvision import transforms          # For pre-processing 
from torch.nn import functional as F        # For final softmax activation

# ML Models are weights + code! When loading in ckpt, need the model as well.
from .model import Model

class Inference(object):
  def __init__(self, class_mapping, params):
    self.class_mapping = class_mapping
    self.hparams = params
    self.transform = transforms.Compose([ 
                      transforms.Resize([self.hparams['length'], self.hparams['width']]),
                      transforms.ToTensor(),
                      transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5,0.5,0.5))
                    ])

  def __call__(self, data_path, ckpt_path):
    model = self._load_model(ckpt_path)
    image_dict = self._load_PIL(data_path)
    output = model(image_dict['tensors'])
    labels = self._translate_output(output)
    return {"PIL_Images": image_dict['PIL_Images'], "labels": labels}

  # Utilities 
  def _load_model(self, ckpt_path): 
    model = Model.load_from_checkpoint(checkpoint_path=ckpt_path)
    model.eval()
    return model

  def _load_PIL(self, data_path): 
    basepath = Path(data_path)
    file_objs = basepath.iterdir()
    images = []
    batch_tensors = []
    for obj in file_objs:
      # Load & Transform 
      img = Image.open(basepath / obj.name)
      img = img.convert('RGB')
      tensor = self.transform(img)
      # Store
      images.append(img)
      batch_tensors.append(tensor)
    return {"PIL_Images": images, "tensors": torch.stack(batch_tensors)}

  def _translate_output(self, one_hot_output):
    class_names = []
    for vector in one_hot_output:
      vector = F.softmax(vector, dim=0)  # Map logits onto [0, 1] range
      id = torch.argmax(vector).item()   # Get index of maximum value
      class_name = list(self.class_mapping.items())[id][0]   # Get corresponding class name at index
      class_names.append(class_name)     # Generate the output
    return class_names