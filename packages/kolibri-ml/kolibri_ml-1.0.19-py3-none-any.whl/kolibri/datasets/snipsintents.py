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

URL = "https://www.dropbox.com/s/somo7vz6p23e2aq/snips_intent.tgz?dl=1"

MD5 = 'c8c7a479b4baf32dcd8e3d7592b32351'

train_files = [
    "AddToPlaylist/train_AddToPlaylist_full.json",
    "BookRestaurant/train_BookRestaurant_full.json",
    "GetWeather/train_GetWeather_full.json",
    "PlayMusic/train_PlayMusic_full.json",
    "RateBook/train_RateBook_full.json",
    "SearchCreativeWork/train_SearchCreativeWork_full.json",
    "SearchScreeningEvent/train_SearchScreeningEvent_full.json",
]
test_files = [
    "AddToPlaylist/validate_AddToPlaylist.json",
    "BookRestaurant/validate_BookRestaurant.json",
    "GetWeather/validate_GetWeather.json",
    "PlayMusic/validate_PlayMusic.json",
    "RateBook/validate_RateBook.json",
    "SearchCreativeWork/validate_SearchCreativeWork.json",
    "SearchScreeningEvent/validate_SearchScreeningEvent.json",
]

NUM_LINES = {
    'train': 560000,
    'test': 70000,
}

_PATH = 'snips_intent.tgz'

DATASET_NAME = "snips_intents"


@_add_docstring_header(num_lines=NUM_LINES)
@_create_dataset_directory(dataset_name=DATASET_NAME)
@_wrap_split_argument(('train', 'test'))
def SnipsIntents(root, split):
    # Create a dataset specific subfolder to deal with generic download filenames
    dataset_tar = download_from_url(URL, root=root,
                                    path=os.path.join(root, _PATH),
                                    hash_value=MD5, hash_type='md5')
    extracted_files = extract_archive(dataset_tar)

    data_filename = _find_match(split + '.txt', extracted_files)
    return TorchDataset(DATASET_NAME, NUM_LINES[split],
                        _create_data_from_csv(data_filename))


if __name__ == '__main__':
    from kolibri.datasets import SnipsIntents

    train_iter = SnipsIntents(split='train')
    for text, pos, tag, _ in train_iter:
        print(text, pos, tag)
