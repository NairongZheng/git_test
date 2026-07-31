# TaskFlow Git 工作流示例

TaskFlow 是一个面向 Git 初学者的教学仓库。项目本身是一个使用 Python
标准库实现的命令行任务管理器，仓库历史用于演示团队项目中的分支、合并、
发布和热修复流程。

当前基线只包含项目骨架和 JSON 数据存储能力，业务功能将在功能分支中逐步实现。

## 快速开始

```bash
python3 main.py --help
python3 -m unittest discover -s tests -v
```

## 分支约定

- `main`：可发布的生产代码。
- `develop`：下一版本的集成分支。
- `feature/*`：从 `develop` 创建的新功能分支。
- `bugfix/*`：从 `develop` 创建的未发布缺陷修复分支。
- `release/*`：从 `develop` 创建的发布准备分支。
- `hotfix/*`：从 `main` 创建的生产紧急修复分支。

