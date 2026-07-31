import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from taskflow.cli import main


class CommandLineTest(unittest.TestCase):
    """验证命令行入口的用户可见行为。"""

    def test_delete_missing_task_returns_controlled_error(self) -> None:
        """删除不存在的任务时应返回错误码而不是异常退出。"""

        with tempfile.TemporaryDirectory() as directory:
            data_file = Path(directory) / "tasks.json"
            output = StringIO()

            with redirect_stdout(output):
                exit_code = main(
                    ["--data-file", str(data_file), "delete", "99"]
                )

            self.assertEqual(exit_code, 1)
            self.assertEqual(output.getvalue().strip(), "未找到任务 #99")


if __name__ == "__main__":
    unittest.main()
