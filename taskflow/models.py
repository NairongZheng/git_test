from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Task:
    """表示一条任务记录。"""

    task_id: int
    title: str
    completed: bool = False

    def to_dict(self) -> dict[str, Any]:
        """将任务转换为可序列化的字典。"""

        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """从字典恢复任务对象。"""

        return cls(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            completed=bool(data.get("completed", False)),
        )
