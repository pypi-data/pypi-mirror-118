import os
from glob import glob
from typing import Any
from typing import Iterable, Iterator

import numpy as np
import tensorflow as tf
from tensorflow import keras
import kolibri.indexers.multi_target_indexer
import kolibri.indexers.multi_content_indexer

class TFDataset(keras.utils.Sequence):
    def __init__(self, x_values, y_values, content_indexer=None, label_indexer=None, x_augmentor=None, batch_size=1,
                 shuffle=False):
        self.y_values = y_values  # array of y_values
        self.x_values = x_values  # array of image paths
        self.batch_size = batch_size  # batch size
        self.shuffle = shuffle  # shuffle bool
        self.on_epoch_end()
        self.content_indexer = content_indexer
        self.label_indexer = label_indexer
        self.augmentor = x_augmentor

    def __len__(self):
        'Denotes the number of batches per epoch'

        if self.x_values is not None:
            return max(1, int(np.ceil(len(self.x_values) / self.batch_size)))
        else:
            return max(1, int(np.ceil(len(self.y_values) / self.batch_size)))

    def set_batch_size(self, new_batch_size):
        self.batch_size = new_batch_size

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        if self.x_values is not None:
            self.indexes = np.arange(len(self.x_values))
        else:
            self.indexes = np.arange(len(self.y_values))

        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __getitem__(self, index):
        'Generate one batch of texts'
        # selects indices of texts for next batch
        indexes = self.indexes[index * self.batch_size: (index + 1) * self.batch_size]

        # select texts and load images
        labels = None
        content = None

        if self.y_values is not None:
            labels = np.array([self.y_values[k] for k in indexes])
            if self.label_indexer:
                labels = self.label_indexer.transform(labels)
            if self.batch_size == 1:
                if isinstance(self.label_indexer, kolibri.indexers.multi_target_indexer.MultiTargetIndexer):
                    labels = [l[0] for l in labels]
                else:
                    labels = labels[0]
        if self.x_values is not None:
            # preprocess and augment texts

            content = [self.x_values[k] for k in indexes]
            if self.augmentor:
                content = self.augmentor(content)

            if self.content_indexer:
                content = self.content_indexer.transform(content)

            if self.batch_size == 1:
                if isinstance(self.content_indexer, kolibri.indexers.multi_content_indexer.MultiContentIndexer):
                    content = [c[0] for c in content]
                else:
                    content = content[0]
        #           content = np.array(content)
        return content, labels
