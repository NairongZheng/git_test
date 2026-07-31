from taskflow.repository import JsonTaskRepository
from taskflow.models import Task


class TaskService:
    """封装任务管理的业务操作。"""

    def __init__(self, repository: JsonTaskRepository) -> None:
        """初始化服务并注入数据仓库。"""

        self._repository = repository

    def list_tasks(self) -> list[Task]:
        """按任务编号返回全部任务。"""

        return sorted(self._repository.load(), key=lambda task: task.task_id)
