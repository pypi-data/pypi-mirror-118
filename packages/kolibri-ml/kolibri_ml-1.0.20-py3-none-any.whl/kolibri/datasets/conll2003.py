from kdmt.download import download_from_url
from kdmt.file import extract_archive

from kolibri.datasets.datasets_utils import (
    _wrap_split_argument,
    _add_docstring_header,
    _find_match,
    _create_dataset_directory,
    _create_data_from_iob,
)
import os
from kolibri.backend.torch.data.generator import TorchDataset

URL = 'https://www.dropbox.com/s/c65bzd23ho73c0l/conll2003.tar.gz?dl=1'

MD5 = '2d99e8b6fd562dc4f750f9c71dbe80c0'

NUM_LINES = {
    'train': 560000,
    'test': 70000,
}

_PATH = 'conll2003_en.tar.gz'

DATASET_NAME = "CoNLL2003"


@_add_docstring_header(num_lines=NUM_LINES)
@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(('train', 'test', 'valid'))
def CoNLL2003(root, split):
    # Create a dataset specific subfolder to deal with generic download filenames
    dataset_tar = download_from_url(URL, root=root,
                                    path=os.path.join(root, _PATH),
                                    hash_value=MD5, hash_type='md5')
    extracted_files = extract_archive(dataset_tar)

    data_filename = _find_match(split + '.txt', extracted_files)
    return TorchDataset(DATASET_NAME, NUM_LINES[split],
                        _create_data_from_iob(data_filename, " "))


if __name__ == '__main__':
    from kolibri.datasets import CoNLL2003

    train_iter = CoNLL2003(split='train')
    for text, pos, tag, _ in train_iter:
        print(text, pos, tag)
