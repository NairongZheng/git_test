import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """创建命令行参数解析器。"""

    return argparse.ArgumentParser(
        prog="taskflow",
        description="一个用于演示 Git 工作流的任务管理器",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """解析命令行参数并执行对应操作。"""

    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0
