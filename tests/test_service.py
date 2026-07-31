import tempfile
import unittest
from pathlib import Path

from taskflow.models import Task
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

    def test_complete_task_updates_existing_task(self) -> None:
        """完成任务时应保存完成状态。"""

        with tempfile.TemporaryDirectory() as directory:
            repository = JsonTaskRepository(Path(directory) / "tasks.json")
            service = TaskService(repository)
            task = service.add_task("完成发布")

            completed_task = service.complete_task(task.task_id)

            self.assertIsNotNone(completed_task)
            self.assertTrue(repository.load()[0].completed)

    def test_complete_task_returns_none_for_missing_task(self) -> None:
        """任务不存在时不应修改数据。"""

        with tempfile.TemporaryDirectory() as directory:
            repository = JsonTaskRepository(Path(directory) / "tasks.json")
            service = TaskService(repository)

            self.assertIsNone(service.complete_task(99))
            self.assertEqual(repository.load(), [])

    def test_delete_task_removes_existing_task(self) -> None:
        """删除任务后数据中不应再包含该任务。"""

        with tempfile.TemporaryDirectory() as directory:
            repository = JsonTaskRepository(Path(directory) / "tasks.json")
            service = TaskService(repository)
            first_task = service.add_task("保留任务")
            deleted_task = service.add_task("删除任务")

            result = service.delete_task(deleted_task.task_id)

            self.assertEqual(result, deleted_task)
            self.assertEqual(repository.load(), [first_task])


if __name__ == "__main__":
    unittest.main()
