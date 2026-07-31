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

    add_parser = subparsers.add_parser("add", help="新增任务")
    add_parser.add_argument("title", help="任务标题")
    subparsers.add_parser("list", help="查看任务")
    complete_parser = subparsers.add_parser("complete", help="完成任务")
    complete_parser.add_argument("task_id", type=int, help="任务编号")
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("task_id", type=int, help="任务编号")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """解析命令行参数并执行对应操作。"""

    parser = build_parser()
    arguments = parser.parse_args(argv)
    service = TaskService(JsonTaskRepository(arguments.data_file))

    if arguments.command == "add":
        try:
            task = service.add_task(arguments.title)
        except ValueError as error:
            print(error)
            return 1
        print(f"已新增任务 #{task.task_id}: {task.title}")
    elif arguments.command == "list":
        tasks = service.list_tasks()
        if not tasks:
            print("暂无任务")
            return 0

        for task in tasks:
            status = "x" if task.completed else " "
            print(f"[{status}] #{task.task_id} {task.title}")
    elif arguments.command == "complete":
        task = service.complete_task(arguments.task_id)
        if task is None:
            print(f"未找到任务 #{arguments.task_id}")
            return 1
        print(f"已完成任务 #{task.task_id}: {task.title}")
    elif arguments.command == "delete":
        task = service.delete_task(arguments.task_id)
        if task is None:
            print(f"未找到任务 #{arguments.task_id}")
            return 1
        print(f"已删除任务 #{task.task_id}: {task.title}")

    return 0
