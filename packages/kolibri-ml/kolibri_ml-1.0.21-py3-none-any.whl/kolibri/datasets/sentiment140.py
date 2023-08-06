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

URL = "https://www.dropbox.com/s/egk8cwupfs05g00/Sentiments140.tar.gz?dl=1"

MD5 = '6b1db4a1d6b9a2d34fa263725f50172c'

NUM_LINES = {
    'all': 1600000,
    'sample': 10000,
}

_PATH = 'Sentiments140.tar.gz'

DATASET_NAME = "Sentiments140"


@_add_docstring_header(num_lines=NUM_LINES)
@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(('all', 'sample'))
def Sentiment140(root, split):
    # Create a dataset specific subfolder to deal with generic download filenames
    dataset_tar = download_from_url(URL, root=root,
                                    path=os.path.join(root, _PATH),
                                    hash_value=MD5, hash_type='md5')
    extracted_files = extract_archive(dataset_tar)

    data_filename = _find_match(split + '.csv', extracted_files)
    return TorchDataset(DATASET_NAME, NUM_LINES[split],
                        _create_data_from_csv(data_filename))


if __name__ == '__main__':


    train_iter = Sentiment140(split='sample')
    for text, pos in train_iter:
        print(text, pos)
