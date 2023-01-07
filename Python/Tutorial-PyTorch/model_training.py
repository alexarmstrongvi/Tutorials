"""
Example PyTorch model creation, training, evaluating, saving, and loading

Most code is copied from https://pytorch.org/tutorials/beginner/basics/quickstart_tutorial.html
"""

import math
from pathlib import Path
from typing import Callable, Literal

import numpy as np
import torch
from torch import nn, Tensor, FloatTensor
from torch.utils.data import DataLoader
#from torch.utils.tensorboard import SummaryWriter
from tensorboardX import SummaryWriter
from torchvision import datasets
from torchvision.transforms import ToTensor

# Globals
CHECKPOINT_DIR_NAME = 'checkpoints'

# Type aliases
LossTensor = FloatTensor # shape=(1,)
LossFunc = Callable[[Tensor, Tensor], LossTensor] # return Tensor shape=(1,)
DeviceLiteral = Literal['cpu', 'cuda']

def main():
    # Configuration
    n_epochs            = 5
    batch_size          = 64
    init_opt_lr         = 1e-3
    # epoch intervals
    checkpoint_interval = 2
    # batch intervals
    val_interval        = None
    log_interval        = 100
    # paths
    odir                = Path('./torch_outputs')
    checkpoint_path     = odir/CHECKPOINT_DIR_NAME

    # Create data loaders.
    training_data, test_data = get_data()
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)

    for X, y in test_dataloader:
        print(f"Shape of X [N, C, H, W]: {X.shape}")
        print(f"Shape of y: {y.shape} [dtype={y.dtype}]")
        break

    # Creating the model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")

    model = NeuralNetwork().to(device)
    print(model)

    # Optimizing the model parameters
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=init_opt_lr)

    start_epoch = 0
    if checkpoint_path:
        if checkpoint_path.is_dir() and any(checkpoint_path.iterdir()):
            checkpoint_path = get_latest_checkpoint(checkpoint_path)
        if checkpoint_path.is_file():
            checkpoint = torch.load(checkpoint_path)
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            start_epoch = checkpoint['epoch'] + 1
            #loss = checkpoint['loss']

    writer = SummaryWriter(odir/'tensorboard_logdir')
    train(
        model               = model,
        train_dataloader    = train_dataloader,
        val_dataloader      = test_dataloader,
        loss_fn             = loss_fn,
        optimizer           = optimizer,
        odir                = odir,
        n_epochs            = n_epochs,
        start_epoch         = start_epoch,
        checkpoint_interval = checkpoint_interval,
        val_interval        = val_interval,
        log_interval        = log_interval,
        device              = device,
        writer              = writer,
    )

    # Saving the model
    model_path      = odir/"model.pth"
    state_dict_path = odir/"model_state_dict.pth"
    # Saving the entire model
    torch.save(model, model_path)
    # Saving the learned parameters (a.k.a. weights and biases)
    torch.save(model.state_dict(), state_dict_path)
    print("Saved PyTorch Model and Model State Dict")

    # Loading the model
    # Load entire model
    model1 = torch.load(model_path)
    # Load state dict into initialized model
    model2 = NeuralNetwork()
    model2.load_state_dict(torch.load(state_dict_path))
    print("Loaded PyTorch Model and Model State Dict")

    # Choose either for evaluation
    eval_model = model2

    # Evaluating model
    classes = [
        "T-shirt/top",
        "Trouser",
        "Pullover",
        "Dress",
        "Coat",
        "Sandal",
        "Shirt",
        "Sneaker",
        "Bag",
        "Ankle boot",
    ]

    x, y = test_data[0][0], test_data[0][1]
    eval_model.eval()
    with torch.no_grad():
        pred = eval_model(x)
        predicted, actual = classes[pred[0].argmax(0)], classes[y]
        print(f'Predicted: "{predicted}", Actual: "{actual}"')

# Define model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):
        # if self.training:
        #     print('Calling forward() in train mode')
        # else:
        #     print('Calling forward() in eval mode')
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

    # If inference requires a slow preprocessing step and one wants to avoid
    # this while developing the model and tuning hyperparameters, the below
    # refactoring of forward() may help. It assumes preprocess() can be run on
    # the data and the results saved for training. Then simply comment out
    # self.preprocess() in forward() below. However, make sure to uncomment
    # preprocess() when saving the model so that all layers, weights, and biases
    # are included.

    # def preprocess(self, x):
    #     return self.flatten
    # def forward_after_preprocessing(self, x):
    #     logits = self.linear_relu_stack(x)
    #     return logits
    # def forward(self, x):
    #     # Comment out preprocess() when training with preprocessed data.
    #     # x = self.preprocess(x)
    #     return self.forward_after_preprocessing(x)

def train(
    model              : nn.Module,
    train_dataloader   : DataLoader,
    val_dataloader     : DataLoader,
    loss_fn            : LossFunc,
    optimizer          : torch.optim.Optimizer,
    odir               : Path,
    n_epochs           : int           = 1,
    start_epoch        : int           = 1,
    checkpoint_interval: int           = 1,
    val_interval       : int           = None,
    log_interval       : int           = 1,
    device             : DeviceLiteral = 'cpu',
    writer             : SummaryWriter = None,
) -> None:
    """Train and evaluate model"""
    n_train_entries = len(train_dataloader.dataset)
    n_train_batches = math.ceil(n_train_entries / train_dataloader.batch_size)

    if val_interval is None:
        val_interval = n_train_batches

    # Setup output folder
    odir.mkdir(exist_ok=True)
    chkpt_dir = odir / CHECKPOINT_DIR_NAME
    chkpt_dir.mkdir(exist_ok=True)

    for epoch_idx in range(start_epoch-1, n_epochs):
        print(f"Epoch {epoch_idx+1}\n-------------------------------")

        # Declare/Initialize
        X   : Tensor
        y   : Tensor # ndim = 1
        loss: Tensor # shape=(1,)
        running_loss = 0.0

        # Train
        model.train()
        for batch_idx, (X, y) in enumerate(train_dataloader):
            X, y = X.to(device), y.to(device)

            # Compute prediction error
            pred = model(X)
            loss = loss_fn(pred, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            global_step    = epoch_idx * n_train_batches + batch_idx
            is_first_batch = (batch_idx == 0)
            is_last_batch  = (batch_idx+1 == n_train_batches)
            is_log_batch   = ((batch_idx % log_interval)+1 == log_interval)
            is_val_batch   = ((batch_idx % val_interval)+1 == val_interval)

            if is_log_batch or is_first_batch or is_last_batch:
                # Log current training metrics
                loss = loss.item()
                entry = batch_idx * train_dataloader.batch_size + len(X)
                print(f"loss: {loss:>7f}  "
                      f"[{entry:>5d}/{n_train_entries:>5d}; "
                      f"{batch_idx+1:>5d}/{n_train_batches}]"
                )

                # Log results to TensorBoard
                avg_loss = running_loss / ((batch_idx % log_interval)+1)
                writer.add_scalars(
                    main_tag        = 'Training vs. Validation Loss',
                    tag_scalar_dict = {'Training' : avg_loss},
                    global_step     = global_step
                )

                # Reset counters
                running_loss = 0

            if is_val_batch or is_last_batch:
                avg_loss, acc = evaluate(model, val_dataloader, loss_fn, device)
                print("Test Error:")
                print(f"\tAccuracy: {(100*acc):>0.1f}%")
                print(f"\tAvg loss: {avg_loss:>8f}")

                writer.add_scalars(
                    main_tag        = 'Training vs. Validation Loss',
                    tag_scalar_dict = {'Validation' : acc},
                    global_step     = global_step,
                )

        is_last_epoch       = (epoch_idx+1 == n_epochs)
        is_checkpoint_epoch = ((epoch_idx % checkpoint_interval)+1 == checkpoint_interval)
        if is_checkpoint_epoch or is_last_epoch:
            chkpt_path = chkpt_dir / f'epoch_{epoch_idx+1:04}.pth'
            save_model_checkpoint(
                model     = model,
                optimizer = optimizer,
                epoch     = epoch_idx+1,
                loss      = loss,
                path      = chkpt_path,
            )
    print("Done!")

def evaluate(
    model           : nn.Module,
    dataloader  : DataLoader,
    loss_fn         : LossFunc,
    device          : DeviceLiteral,
) -> tuple[float, float]:
    """Evaluate model performance"""
    running_loss, n_correct = 0.0, 0

    with torch.no_grad():
        X: Tensor
        y: Tensor # ndim = 1
        model.eval()
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred: Tensor = model(X)
            running_loss += loss_fn(pred, y).item()
            n_correct += (pred.argmax(1) == y).sum().item()
        model.train()

    n_val_entries = len(dataloader.dataset)
    n_val_batches = math.ceil(n_val_entries / dataloader.batch_size)
    avg_loss      = running_loss / n_val_batches
    accuracy      = n_correct / n_val_entries
    return avg_loss, accuracy

def save_model_checkpoint(
    model    : nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch    : int,
    loss     : Tensor,
    path     : Path,
) -> None:
    obj = {
        'epoch'               : epoch,
        'model_state_dict'    : model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss'                : loss
    }
    torch.save(obj, path)

def get_latest_checkpoint(path : Path) -> Path:
    return sorted(path.iterdir())[-1]

def get_data() -> tuple[np.ndarray, np.ndarray]:
    # Download training data from open datasets.
    training_data = datasets.FashionMNIST(
        root="data",
        train=True,
        download=True,
        transform=ToTensor(),
    )

    # Download test data from open datasets.
    test_data = datasets.FashionMNIST(
        root="data",
        train=False,
        download=True,
        transform=ToTensor(),
    )
    return training_data, test_data

if __name__ == '__main__':
    main()