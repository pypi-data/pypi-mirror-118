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

URL = "https://www.dropbox.com/s/8a1pm3gg9e5szso/consumer_complaints.tar.gz?dl=1"

MD5 = 'c8c7a479b4baf32dcd8e3d7592b32351'

NUM_LINES = {
    'train': 560000,
    'test': 70000,
}

_PATH = 'consumer_complaints.tar.gz'

DATASET_NAME = "consumer_complaints"


@_add_docstring_header(num_lines=NUM_LINES)
@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(('train', 'test'))
def ConsumerComplaints(root, split):
    # Create a dataset specific subfolder to deal with generic download filenames
    dataset_tar = download_from_url(URL, root=root,
                                    path=os.path.join(root, _PATH),
                                    hash_value=MD5, hash_type='md5')
    extracted_files = extract_archive(dataset_tar)

    data_filename = _find_match(split + '.csv', extracted_files)
    return TorchDataset(DATASET_NAME, NUM_LINES[split],
                        _create_data_from_csv(data_filename))


if __name__ == '__main__':
    from kolibri.datasets import ConsumerComplaints

    train_iter = ConsumerComplaints(split='train')
    for text, pos in train_iter:
        print(text, pos)
