import tempfile
import unittest
from pathlib import Path

from taskflow.repository import JsonTaskRepository
from taskflow.service import TaskService


class TaskServiceTest(unittest.TestCase):
    """验证任务业务服务。"""

    def test_add_task_assigns_incrementing_ids(self) -> None:
        """新增任务时应自动生成递增编号。"""

        with tempfile.TemporaryDirectory() as directory:
            repository = JsonTaskRepository(Path(directory) / "tasks.json")
            service = TaskService(repository)

            first_task = service.add_task("设计接口")
            second_task = service.add_task("补充测试")

            self.assertEqual(first_task.task_id, 1)
            self.assertEqual(second_task.task_id, 2)
            self.assertEqual(repository.load(), [first_task, second_task])


if __name__ == "__main__":
    unittest.main()
