import json
import tempfile
import unittest
from pathlib import Path

from taskflow.models import Task
from taskflow.repository import JsonTaskRepository


class JsonTaskRepositoryTest(unittest.TestCase):
    """验证 JSON 任务仓库。"""

    def test_load_returns_empty_list_when_file_missing(self) -> None:
        """数据文件不存在时应返回空列表。"""

        with tempfile.TemporaryDirectory() as directory:
            repository = JsonTaskRepository(Path(directory) / "tasks.json")

            self.assertEqual(repository.load(), [])

    def test_save_and_load_tasks(self) -> None:
        """保存后应能够恢复相同任务。"""

        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "tasks.json"
            repository = JsonTaskRepository(data_file)
            tasks = [Task(task_id=1, title="学习 Git")]

            repository.save(tasks)

            self.assertEqual(repository.load(), tasks)
            self.assertEqual(
                json.loads(data_file.read_text(encoding="utf-8"))[0]["title"],
                "学习 Git",
            )


if __name__ == "__main__":
    unittest.main()
