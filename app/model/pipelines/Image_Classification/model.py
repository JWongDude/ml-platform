# model.py 
# Image Classification Model 
import torch                                      # For utility
from torch import nn                              # For layers
from torch.nn import functional as F              # For loss, activation functions
import torchvision.models as models               # For transfer learning
import torchmetrics                               # For metrics 
from pytorch_lightning.core.lightning import LightningModule  # For model

# Transfer Learning with ResNet50 feature extractor. 
# Head replaced with n-node fc layer with softmax activation.
class Model(LightningModule):
  def __init__(self, params):
    super().__init__()
    self.hparams = params

    # Create backbone
    backbone = models.resnet50(pretrained=True)
    num_filters = backbone.fc.in_features
    layers = list(backbone.children())[:-1]  
    self.feature_extractor = nn.Sequential(*layers)

    # Create head, the only layer that is learned
    self.classifer = nn.Linear(num_filters, self.hparams['num_classes'])

    # Define metrics
    self.train_acc = torchmetrics.Accuracy()
    self.valid_acc = torchmetrics.Accuracy()

  def forward(self, x):
    # Use Resnet backbone
    self.feature_extractor.eval() 
    with torch.no_grad():
      representations = self.feature_extractor(x).flatten(1)

    # Learn head
    x = self.classifer(representations) 
    return x  

  def configure_optimizers(self):
    return torch.optim.Adam(self.parameters(), self.hparams['lr'])

  def training_step(self, batch, batch_idx):
    x, y = batch 
    logits = self(x)
    loss = F.cross_entropy(logits, y) # One hot encoding, log_softmax interally
    preds = F.softmax(logits, dim=1)
    self.train_acc(preds, y)

    self.log('train_loss', loss)
    self.log('train_acc', self.train_acc)
    return loss  # Mandatory

  def validation_step(self, batch, batch_idx):
    x, y = batch 
    logits = self(x)
    loss = F.cross_entropy(logits, y)
    preds = F.softmax(logits, dim=1)
    self.valid_acc(preds, y)

    self.log('val_loss', loss)
    self.log('val_acc', self.valid_acc)

  # Define default parameters
  @staticmethod
  def add_model_specific_args(parent_parser):
    parser = parent_parser.add_argument_group('Model Params')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning Rate, typical range [0.1 - 1e-5]')
    return parent_parser