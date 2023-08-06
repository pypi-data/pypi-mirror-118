'''Utility functions to be used in other scripts'''

from functools import wraps
from typing import Callable
import warnings
import datasets.utils.logging as ds_logging
import logging
import pkg_resources
import re
import transformers.utils.logging as tf_logging
import torch
from transformers import (AutoModelForTokenClassification,
                          AutoModelForSequenceClassification,
                          TFAutoModelForTokenClassification,
                          TFAutoModelForSequenceClassification,
                          FlaxAutoModelForTokenClassification,
                          FlaxAutoModelForSequenceClassification,
                          Trainer)

PT_CLS = {'token-classification': AutoModelForTokenClassification,
          'text-classification': AutoModelForSequenceClassification}
TF_CLS = {'token-classification': TFAutoModelForTokenClassification,
          'text-classification': TFAutoModelForSequenceClassification}
JAX_CLS = {'token-classification': FlaxAutoModelForTokenClassification,
           'text-classification': FlaxAutoModelForSequenceClassification}
MODEL_CLASSES = dict(pytorch=PT_CLS, tensorflow=TF_CLS, jax=JAX_CLS)


class TwolabelTrainer(Trainer):
    '''Trainer class which deals with two labels.'''
    def __init__(self, split_point: int, **kwargs):
        self.split_point = split_point
        super().__init__(**kwargs)

    def compute_loss(self, model, inputs, return_outputs=False):
        labels = inputs.pop('labels')
        labels1 = labels[:, :, 0]
        labels2 = labels[:, :, 1]
        labels2 = torch.where(labels2 > 0, labels2 - self.split_point, labels2)

        outputs = model(**inputs)
        logits = outputs.logits

        logits1 = logits[:, :, :self.split_point]
        logits2 = logits[:, :, self.split_point:]
        num_classes2 = logits2.size(2)

        loss_fct = torch.nn.CrossEntropyLoss()
        loss1 = loss_fct(logits1.view(-1, self.split_point),
                         labels1.view(-1))
        loss2 = loss_fct(logits2.view(-1, num_classes2),
                         labels2.view(-1))
        loss = loss1 + loss2
        return (loss, outputs) if return_outputs else loss


class InvalidBenchmark(Exception):
    def __init__(self, message: str = 'This model cannot be benchmarked '
                                      'on the given dataset.'):
        self.message = message
        super().__init__(self.message)


def is_module_installed(module: str) -> bool:
    '''Check if a module is installed.

    Args:
        module (str): The name of the module.

    Returns:
        bool: Whether the module is installed or not.
    '''
    installed_modules_with_versions = list(pkg_resources.working_set)
    installed_modules = [re.sub('[0-9. ]', '', str(module))
                         for module in installed_modules_with_versions]
    installed_modules_processed = [module.lower().replace('-', '_')
                                   for module in installed_modules]
    return module.lower() in installed_modules_processed


def block_terminal_output():
    '''Blocks libraries from writing output to the terminal'''

    # Ignore miscellaneous warnings
    warnings.filterwarnings('ignore',
                            module='torch.nn.parallel*',
                            message=('Was asked to gather along dimension 0, '
                                     'but all input tensors were scalars; '
                                     'will instead unsqueeze and return '
                                     'a vector.'))
    warnings.filterwarnings('ignore', module='seqeval*')

    logging.getLogger('filelock').setLevel(logging.ERROR)

    # Disable the tokenizer progress bars
    ds_logging.get_verbosity = lambda: ds_logging.NOTSET

    # Disable most of the `transformers` logging
    tf_logging.set_verbosity_error()


class DocInherit(object):
    '''Docstring inheriting method descriptor.

    The class itself is also used as a decorator.
    '''
    def __init__(self, mthd: Callable):
        self.mthd = mthd
        self.name = mthd.__name__

    def __get__(self, obj, cls):
        if obj:
            return self.get_with_inst(obj, cls)
        else:
            return self.get_no_inst(cls)

    def get_with_inst(self, obj, cls):

        overridden = getattr(super(cls, obj), self.name, None)

        @wraps(self.mthd, assigned=('__name__', '__module__'))
        def f(*args, **kwargs):
            return self.mthd(obj, *args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def get_no_inst(self, cls):
        for parent in cls.__mro__[1:]:
            overridden = getattr(parent, self.name, None)
            if overridden:
                break

        @wraps(self.mthd, assigned=('__name__', '__module__'))
        def f(*args, **kwargs):
            return self.mthd(*args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def use_parent_doc(self, func, source):
        if source is None:
            raise NameError(f'Can\'t find "{self.name}" in parents')
        func.__doc__ = source.__doc__
        return func


doc_inherit = DocInherit
