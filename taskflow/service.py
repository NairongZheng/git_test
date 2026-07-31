from taskflow.repository import JsonTaskRepository
from taskflow.models import Task


class TaskService:
    """封装任务管理的业务操作。"""

    def __init__(self, repository: JsonTaskRepository) -> None:
        """初始化服务并注入数据仓库。"""

        self._repository = repository

    def add_task(self, title: str) -> Task:
        """创建任务并返回保存后的记录。"""

        tasks = self._repository.load()
        next_id = max((task.task_id for task in tasks), default=0) + 1
        task = Task(task_id=next_id, title=title)
        self._repository.save([*tasks, task])
        return task
