from dataclasses import replace

from taskflow.models import Task
from taskflow.repository import JsonTaskRepository


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

    def list_tasks(self) -> list[Task]:
        """按任务编号返回全部任务。"""

        return sorted(self._repository.load(), key=lambda task: task.task_id)

    def complete_task(self, task_id: int) -> Task | None:
        """将指定任务标记为完成；任务不存在时返回空值。"""

        tasks = self._repository.load()
        for index, task in enumerate(tasks):
            if task.task_id != task_id:
                continue

            completed_task = replace(task, completed=True)
            tasks[index] = completed_task
            self._repository.save(tasks)
            return completed_task

        return None
