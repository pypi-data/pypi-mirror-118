import logging
import os
import torch
from torch.nn.modules import Module
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]\t%(asctime)s\t\t %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def build_checkpoint_path(root, platform, name, *tags):
    return "." + os.path.join(root, platform, *tags, name)


class AgentBase(ABC):
    CHECKPOINT_DIR_NAME = 'checkpoint_dir'
    PYTORCH_PLATFORM = '/pytorch'
    KERAS_PLATFORM = '/keras'
    FILENAME = "checkpoint"
    SEPARATOR = "-"

    def __init__(self, *args, **kwargs):
        self.checkpoint_dir = "./output/checkpoints"
        if AgentBase.CHECKPOINT_DIR_NAME in kwargs:
            self.checkpoint = kwargs[AgentBase.CHECKPOINT_DIR_NAME]

    def override_defaults(self):
        pass

    @abstractmethod
    def before(self, *args, **kwargs):
        pass

    @abstractmethod
    def after(self, *args, **kwargs):
        pass

    @abstractmethod
    def act(self, state) -> int:
        pass

    @abstractmethod
    def learn(self, *args, **kwargs):
        pass

    def get_next_index(self, target_dir):
        if (os.path.exists(target_dir)):
            return len(os.listdir(target_dir))
        return 0

    def init_dir(self, target_dir):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

    def save_pytorch_model(self, model: Module, identifier, *tags):
        save_dir = build_checkpoint_path(AgentBase.CHECKPOINT_DIR_NAME, AgentBase.PYTORCH_PLATFORM, identifier, *tags)
        self.init_dir(save_dir)
        save_path = os.path.join(save_dir,
                                 (AgentBase.FILENAME + AgentBase.SEPARATOR + str(self.get_next_index(save_dir))))
        LOG.info("Saving pytorch model at " + save_path)
        torch.save(model.state_dict(), save_path)

    def load_pytorch_model(self, model: Module, identifier, *tags, checkpoint_number=None):
        load_dir = build_checkpoint_path(AgentBase.CHECKPOINT_DIR_NAME, AgentBase.PYTORCH_PLATFORM, identifier, *tags)
        if not checkpoint_number:
            checkpoint_number = self.get_next_index(load_dir)
        load_path = os.path.join(load_dir, (AgentBase.FILENAME + AgentBase.SEPARATOR + str(checkpoint_number)))
        LOG.info("Loading pytorch model at " + load_path)
        model.load_state_dict(torch.load(load_path))

    def save_keras_model(self):
        pass
