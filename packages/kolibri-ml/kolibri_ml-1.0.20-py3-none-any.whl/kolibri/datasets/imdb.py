from kdmt.download import  download_from_url
from  kdmt.file import extract_archive

from kolibri.data.generators import DataIterator
from kolibri.datasets.datasets_utils import _wrap_split_argument
from kolibri.datasets.datasets_utils import _add_docstring_header
from kolibri.datasets.datasets_utils import _create_dataset_directory
import io

URL = 'http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz'

MD5 = '7c2ac02c03563afcf9b574c7e56c153a'

NUM_LINES = {
    'train': 25000,
    'test': 25000,
}

_PATH = 'aclImdb_v1.tar.gz'

DATASET_NAME = "Imdb"


@_add_docstring_header(num_lines=NUM_LINES, num_classes=2)
@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(('train', 'test'))
def Imdb(root, split):
    def generate_imdb_data(key, extracted_files):
        for fname in extracted_files:
            if 'urls' in fname:
                continue
            elif key in fname and ('pos' in fname or 'neg' in fname):
                with io.open(fname, encoding="utf8") as f:
                    label = 'pos' if 'pos' in fname else 'neg'
                    yield label, f.read()
    dataset_tar = download_from_url(URL, root=root,
                                    hash_value=MD5, hash_type='md5')
    extracted_files = extract_archive(dataset_tar)
    iterator = generate_imdb_data(split, extracted_files)
    return DataIterator(DATASET_NAME, NUM_LINES[split], iterator)



if __name__ =='__main__':
    from kolibri.datasets import Imdb

    train_iter = Imdb(split='train')
    for label, line in train_iter:
        print(label, line)
