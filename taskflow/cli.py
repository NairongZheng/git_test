import argparse
from collections.abc import Sequence
from pathlib import Path

from taskflow.repository import JsonTaskRepository
from taskflow.service import TaskService


def build_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器。"""

    parser = argparse.ArgumentParser(
        prog="taskflow",
        description="一个用于演示 Git 工作流的任务管理器",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=Path(".taskflow.json"),
        help="任务数据文件路径",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="查看任务")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """解析命令行参数并执行对应操作。"""

    parser = build_parser()
    arguments = parser.parse_args(argv)
    service = TaskService(JsonTaskRepository(arguments.data_file))

    if arguments.command == "list":
        tasks = service.list_tasks()
        if not tasks:
            print("暂无任务")
            return 0

        for task in tasks:
            status = "x" if task.completed else " "
            print(f"[{status}] #{task.task_id} {task.title}")

    return 0
