import json
from pathlib import Path

from taskflow.models import Task


class JsonTaskRepository:
    """使用 JSON 文件持久化任务。"""

    def __init__(self, data_file: Path) -> None:
        """初始化仓库并记录数据文件路径。"""

        self._data_file = data_file

    def load(self) -> list[Task]:
        """读取全部任务；数据文件不存在时返回空列表。"""

        if not self._data_file.exists():
            return []

        raw_tasks = json.loads(self._data_file.read_text(encoding="utf-8"))
        return [Task.from_dict(item) for item in raw_tasks]

    def save(self, tasks: list[Task]) -> None:
        """覆盖保存全部任务。"""

        # 先确保父目录存在，便于调用者使用自定义数据路径。
        self._data_file.parent.mkdir(parents=True, exist_ok=True)
        payload = [task.to_dict() for task in tasks]
        self._data_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
