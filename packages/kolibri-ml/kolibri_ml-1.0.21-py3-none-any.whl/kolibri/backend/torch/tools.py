import random, os, torch
import numpy as np
from torch import nn, optim
from typing import Tuple, Dict
from pathlib import Path
import fsspec
import torch
from fsspec.implementations.local import LocalFileSystem

def seed_everything(seed=1029):
    '''
    :param seed:
    :param device:
    :return:
    '''
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    # some cudnn methods can be random even after fixing the seed
    # unless you tell it to be deterministic
    torch.backends.cudnn.deterministic = True


class AverageMeter:
    """
    Keep track of most recent, average, sum, and count of a metric
    """
    def __init__(self, tag = None, writer = None):
        self.writer = writer
        self.tag = tag
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n = 1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

        # tensorboard
        if self.writer is not None:
            self.writer.add_scalar(self.tag, val)


def save_checkpoint(
    epoch: int,
    model: nn.Module,
    model_name: str,
    optimizer: optim.Optimizer,
    dataset_name: str,
    word_map: Dict[str, int],
    checkpoint_path: str,
    checkpoint_basename: str = 'checkpoint'
) -> None:
    """
    Save a model checkpoint

    Parameters
    ----------
    epoch : int
        Epoch number the current checkpoint have been trained for

    model : nn.Module
        Model

    model_name : str
        Name of the model

    optimizer : optim.Optimizer
        Optimizer to update the model's weights

    dataset_name : str
        Name of the dataset

    word_map : Dict[str, int]
        Word2ix map

    checkpoint_path : str
        Path to save the checkpoint

    checkpoint_basename : str
        Basename of the checkpoint
    """
    state = {
        'epoch': epoch,
        'model': model,
        'model_name': model_name,
        'optimizer': optimizer,
        'dataset_name': dataset_name,
        'word_map': word_map
    }
    save_path = os.path.join(checkpoint_path, checkpoint_basename + '.pth.tar')
    torch.save(state, save_path)

def load_checkpoint(
    checkpoint_path: str, device: torch.device
) -> Tuple[nn.Module, str, optim.Optimizer, str, Dict[str, int], int]:
    """
    Load a checkpoint, so that we can continue to train on it

    Parameters
    ----------
    checkpoint_path : str
        Path to the checkpoint to be loaded

    device : torch.device
        Remap the model to which device

    Returns
    -------
    model : nn.Module
        Model

    model_name : str
        Name of the model

    optimizer : optim.Optimizer
        Optimizer to update the model's weights

    dataset_name : str
        Name of the dataset

    word_map : Dict[str, int]
        Word2ix map

    start_epoch : int
        We should start training the model from __th epoch
    """
    checkpoint = torch.load(checkpoint_path, map_location=str(device))

    model = checkpoint['model']
    model_name = checkpoint['model_name']
    optimizer = checkpoint['optimizer']
    dataset_name = checkpoint['dataset_name']
    word_map = checkpoint['word_map']
    start_epoch = checkpoint['epoch'] + 1

    return model, model_name, optimizer, dataset_name, word_map, start_epoch

def clip_gradient(optimizer: optim.Optimizer, grad_clip: float) -> None:
    """
    Clip gradients computed during backpropagation to avoid explosion of gradients.

    Parameters
    ----------
    optimizer : optim.Optimizer
        Optimizer with the gradients to be clipped

    grad_clip : float
        Gradient clip value
    """
    for group in optimizer.param_groups:
        for param in group['params']:
            if param.grad is not None:
                param.grad.data.clamp_(-grad_clip, grad_clip)


def adjust_learning_rate(optimizer: optim.Optimizer, scale_factor: float) -> None:
    """
    Shrink learning rate by a specified factor.

    Parameters
    ----------
    optimizer : optim.Optimizer
        Optimizer whose learning rate must be shrunk

    shrink_factor : float
        Factor in interval (0, 1) to multiply learning rate with
    """
    print("\nDECAYING learning rate.")
    for param_group in optimizer.param_groups:
        param_group['lr'] = param_group['lr'] * scale_factor
    print("The new learning rate is %f\n" % (optimizer.param_groups[0]['lr'],))



def load(path_or_url, map_location=None):
    if not isinstance(path_or_url, (str, Path)):
        # any sort of BytesIO or similiar
        return torch.load(path_or_url, map_location=map_location)
    if str(path_or_url).startswith("http"):
        return torch.hub.load_state_dict_from_url(str(path_or_url), map_location=map_location)
    fs = get_filesystem(path_or_url)
    with fs.open(path_or_url, "rb") as f:
        return torch.load(f, map_location=map_location)


def get_filesystem(path):
    path = str(path)
    if "://" in path:
        # use the fileystem from the protocol specified
        return fsspec.filesystem(path.split(":", 1)[0])
    else:
        # use local filesystem
        return LocalFileSystem()


def atomic_save(checkpoint, filepath: str):
    """Saves a checkpoint atomically, avoiding the creation of incomplete checkpoints.

    Args:
        checkpoint: The object to save.
            Built to be used with the ``dump_checkpoint`` method, but can deal with anything which ``torch.save``
            accepts.
        filepath: The path to which the checkpoint will be saved.
            This points to the file that the checkpoint will be stored in.
    """

    bytesbuffer = io.BytesIO()
    # Can't use the new zipfile serialization for 1.6.0 because there's a bug in
    # torch.hub.load_state_dict_from_url() that prevents it from loading the new files.
    # More details can be found here: https://github.com/pytorch/pytorch/issues/42239
    if Version(torch.__version__).release[:3] == (1, 6, 0):
        torch.save(checkpoint, bytesbuffer, _use_new_zipfile_serialization=False)
    else:
        torch.save(checkpoint, bytesbuffer)
    with fsspec.open(filepath, "wb") as f:
        f.write(bytesbuffer.getvalue())
