import logging
import sys
from abc import ABC
from typing import Type, Dict, Union

from krong.alias import TASK_ALIAS
from krong.task import Task
from krong.tasks.tagger.tasks import Tagger


class TaskFactory(ABC):
    def get(self, name: str) -> Type[Task]:
        """
        Get class of module

        Args:
            name (str): name of module

        Returns:

        """
        name = TASK_ALIAS[name.lower()]
        return self.available_tasks()[name]

    def create(self, name: str, usage: Union[str, bool], **kwargs) -> Task:
        module = self.get(name)
        self._print_usage(name, usage, module)
        return module(**kwargs)

    @staticmethod
    def available_tasks() -> Dict[str, Type[Task]]:
        return {"tagging": Tagger}

    @staticmethod
    def _print_usage(name, usage, module):
        if isinstance(usage, str):
            usage = usage.lower()

        assert usage in [True, False, "en", "ko", "auto"]

        if usage == "auto":
            usage = hasattr(sys, "ps1")

        usage = "ko" if usage is True else usage
        if usage is not False:
            usage_string = module.usage()[usage]

            if usage == "ko":
                usage_string = f"`{name}` 태스크 사용법.\n" + usage_string
            else:
                usage_string = f"The usage of `{name}` task.\n" + usage_string

            logging.warning(usage_string)
