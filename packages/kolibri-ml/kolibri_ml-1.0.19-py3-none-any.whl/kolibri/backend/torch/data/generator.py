import torch
import kolibri

class TorchDataset(torch.utils.data.Dataset)    :
    """Defines an abstraction for raw text iterable datasets.
    """

    def __init__(self,x_values, y_values, content_indexer=None, label_indexer=None,x_augmentor=None):
        """Initiate the dataset abstraction.
        """
        super(TorchDataset, self).__init__()
        self.x_values=x_values
        self.y_values=y_values
        self.num_lines=len(y_values)
        self.current_pos = None
        self.content_indexer = content_indexer
        self.label_indexer = label_indexer
        self.augmentor=x_augmentor
    def reset(self):
        self.current_pos=0

    def __getitem__(self, index):
        'Generate one batch of texts'
        labels = None
        content = None

        if self.y_values is not None:
            labels = self.y_values[index]
            if self.label_indexer:
                labels = self.label_indexer.transform([labels])[0]

        if self.x_values is not None:
            # preprocess and augment texts

            content = self.x_values[index]
            if self.augmentor:
                content = self.augmentor(content)

            if self.content_indexer:
                content = self.content_indexer.transform([content])[0]

        return content, labels



    def __len__(self):
        return self.num_lines

    def pos(self):
        """
        Returns current position of the iterator. This returns None
        if the iterator hasn't been used yet.
        """
        return self.current_pos

    def __str__(self):
        return self.description
