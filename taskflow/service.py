from taskflow.repository import JsonTaskRepository


class TaskService:
    """封装任务管理的业务操作。"""

    def __init__(self, repository: JsonTaskRepository) -> None:
        """初始化服务并注入数据仓库。"""

        self._repository = repository
