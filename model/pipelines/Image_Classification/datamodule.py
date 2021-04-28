# datamodule.py 
# Image Classification Data Preparation
from torchvision import datasets, transforms      # For dataset
from torch.utils.data import DataLoader           # For dataloader
from pytorch_lightning.core.datamodule import LightningDataModule  # For data module

class DataModule(LightningDataModule):
  def __init__(self, hparams):
    super().__init__()
    # Store arguments
    self.hparams = hparams

    # Define transforms
    self.transform = { 
      'train': transforms.Compose([
          transforms.Resize([self.hparams['length'], self.hparams['width']]), 
          transforms.RandomHorizontalFlip(),
          transforms.RandomVerticalFlip(),
          transforms.ToTensor(), # This also auto-normalizes to range [0, 1]
          transforms.Normalize(mean=(0.5,0.5,0.5), std=(0.5,0.5,0.5)) # Assuming Gaussian
      ]),
      'val': transforms.Compose([
          transforms.Resize([self.hparams['length'], self.hparams['width']]),
          transforms.ToTensor(),
          transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5,0.5,0.5))                      
      ])
    }
    
  # Download and split data here, (nothing in this local-data, split case)
  # def prepare_data(self): 
  
  # Make datasets
  def setup(self, stage = None): 
    self.train_data = datasets.ImageFolder(root=self.hparams['input_dirpath'] + '/train', transform=self.transform['train'])
    self.val_data = datasets.ImageFolder(root=self.hparams['input_dirpath'] + '/valid', transform=self.transform['val']) 

    self.class_mapping = self.train_data.class_to_idx  # To pass to inference

  # Make dataloaders
  def train_dataloader(self): 
    return DataLoader(dataset=self.train_data, batch_size=self.hparams['batch_size'], 
                      shuffle=True, num_workers=self.hparams['num_workers'])

  def val_dataloader(self):
    return DataLoader(dataset=self.val_data, batch_size=self.hparams['batch_size'], 
                      shuffle=False, num_workers=1)
  
  # Define default parameters
  @staticmethod
  def add_model_specific_args(parent_parser):
    parser = parent_parser.add_argument_group('Datamodule Params')
    parser.add_argument('--length', type=int, default=224)
    parser.add_argument('--width', type=int, default=224)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--num_workers', type=int, default=2)
    return parent_parser