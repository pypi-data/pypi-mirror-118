from kdmt.download import download_from_url
from kdmt.file import extract_archive

from kolibri.datasets.datasets_utils import (
    _wrap_split_argument,
    _add_docstring_header,
    _find_match,
    _create_dataset_directory,
    _create_data_from_csv,
)
import os
from kolibri.backend.torch.data.generator import TorchDataset

URL = "https://www.dropbox.com/s/7v4tm6lsjkxnvfk/creditcard_fraud.tgz?dl=1"

MD5 = '94c62cf7f761f71c3b179307894fd169'

NUM_LINES = {
    'train': 560000,
    'test': 70000,
}

_PATH = 'creditcard_fraud.tgz'

DATASET_NAME = "creditcard_fraud"


@_add_docstring_header(num_lines=NUM_LINES)
@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(('train', 'test'))
def CreditCardFraud(root, split):
    # Create a dataset specific subfolder to deal with generic download filenames
    dataset_tar = download_from_url(URL, root=root,
                                    path=os.path.join(root, _PATH),
                                    hash_value=MD5, hash_type='md5')
    extracted_files = extract_archive(dataset_tar)

    data_filename = _find_match(split + '.txt', extracted_files)
    return TorchDataset(DATASET_NAME, NUM_LINES[split],
                        _create_data_from_csv(data_filename))


if __name__ == '__main__':
    from kolibri.datasets import CoNLL2003

    train_iter = CreditCardFraud(split='train')
    for text, pos, tag, _ in train_iter:
        print(text, pos, tag)
