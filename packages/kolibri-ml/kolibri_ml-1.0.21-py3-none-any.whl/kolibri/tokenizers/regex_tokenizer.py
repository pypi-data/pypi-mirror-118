import re  # gex as re

from kolibri.tokenizers.tokenizer import Tokenizer
from kdmt.dict import update

# @ray.remote
class RegexpTokenizer(Tokenizer):
    """
    A tokenizer that splits a string using a regular expression, which
    matches either the tokens or the separators between tokens.
    By default, the following flags are
        used: `re.UNICODE | re.MULTILINE | re.DOTALL`.
    """



    def __init__(self, config=None):
        hyperparameters= {
        "fixed": {
            'pattern': r"\b(?:[A-Za-z][@\.A-Za-z-]{2,}|[\w-]{2,}|(?:\d+(?:[\.,:]\d+)*))\b",
            'flags': re.UNICODE | re.MULTILINE
        },

        "tunable": {
        }
    }
        # If they gave us a regexp object, extract the patterns.
        super().__init__(config)
        self.hyperparameters=update(hyperparameters, self.hyperparameters)

        pattern = self.hyperparameters['fixed']['pattern']

        self._flags = self.hyperparameters['fixed']['flags']
        self._regexp = re.compile(pattern, self._flags)

    def __hash__(self):
        return hash(self.name)

    def tokenize(self, text):
        return self._regexp.findall(str(text))

from kolibri.registry import ModulesRegistry
ModulesRegistry.add_module(RegexpTokenizer.name, RegexpTokenizer)



if __name__ == '__main__':
    text = """"Please add the 'Statutory > NL-Sick Leave' => See table below.
    Company
    UPI
    Legal Name - Last Name
    Preferred Name - First Name
    Type of Leave
    Start of Leave
    Estimated Last Day of Leave
    Actual Last Day of Leave
    6079 AbbVie BV Commercial
    10373417
    Bosua
    Rosanna
    Statutory > NL-Sick Leave
    29-APR-2019
    28-APR-2020
    6079 AbbVie BV Commercial
    10355526
    Scholtes
    Monique
    Statutory > NL-Sick Leave
    26-NOV-2018
    25-NOV-2019
    Thanks!
    Met vriendelijke groet"""

    tokenizer = RegexpTokenizer()
    tokens = tokenizer.tokenize(text)
    for t in tokens:
        print(t)
