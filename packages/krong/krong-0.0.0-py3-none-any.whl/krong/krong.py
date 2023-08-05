import logging
from typing import Union

from krong.factory import TaskFactory
from krong.task import Task

logging.basicConfig(
    format="[Korean Language ToolKit]: %(message)s", level=logging.WARNING
)


class Krong(object):
    """
    Korean language processing toolkit based on non-neural methods for general purpose.

    Args:
        task (str): name of the task
        usage (bool): print usage for loading the task object

    Examples:
        >>> # 1. Basic Usage
        >>> from krong import Krong
        >>> tagger = Krong(task="tagger")
        >>> tagger("아버지가방에들어가시다")
        [('아버지', 'NNG'), ('가', 'JKS'), ('방', 'NNG'), ('에', 'JKB'), ('들어가', 'VV'), ('시', 'EP'), ('다', 'EC')]

        >>> # 2. Using `usage` option.
        >>> # You can check the usage of each task via `usage` option for loading task object.
        >>> # option `usage` can be `en`(english) or `ko`(korean) (if you set usage to `True`, it will be `ko`)
        >>> tagger = Krong(task="tagger", usage="ko")
    """

    FACTORY: TaskFactory = TaskFactory()

    def __new__(cls, task: str, usage: Union[str, bool] = "auto", **kwargs) -> Task:
        return Krong.FACTORY.create(name=task, usage=usage, **kwargs)

    @staticmethod
    def available_tasks() -> str:
        """
        Print available tasks

        Returns:
            str: available tasks
        """
        return f"Available tasks are {list(Krong.FACTORY.available_tasks().keys())}."

    @staticmethod
    def usage(task: str, lang: str = "ko") -> str:
        """
        Print usage of the task

        Args:
            task (str): name of the task
            lang (str): language of the usage

        Returns:
            str: usage of the task
        """
        return Krong.FACTORY.get(name=task).usage()[lang]
