import tempfile
import unittest
from pathlib import Path

from taskflow.models import Task
from taskflow.repository import JsonTaskRepository
from taskflow.service import TaskService


class TaskServiceTest(unittest.TestCase):
    """验证任务业务服务。"""

    def test_list_tasks_orders_tasks_by_id(self) -> None:
        """任务列表应按编号升序排列。"""

        with tempfile.TemporaryDirectory() as directory:
            repository = JsonTaskRepository(Path(directory) / "tasks.json")
            repository.save(
                [
                    Task(task_id=2, title="编写文档"),
                    Task(task_id=1, title="设计接口"),
                ]
            )
            service = TaskService(repository)

            tasks = service.list_tasks()

            self.assertEqual([task.task_id for task in tasks], [1, 2])


if __name__ == "__main__":
    unittest.main()
