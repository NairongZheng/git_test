# TaskFlow Git 工作流示例

TaskFlow 是一个面向 Git 初学者的团队协作教学仓库。项目本身是一个使用
Python 标准库实现的命令行任务管理器，重点是通过真实提交历史展示功能开发、
代码集成、版本发布和生产热修复。

> 这是一套便于学习的简化 Git Flow。团队应根据发布频率和协作规模调整流程，
> 不必机械照搬所有分支。

## 项目功能

```bash
# 新增任务
python3 main.py add "学习 feature 分支"

# 查看任务
python3 main.py list

# 完成和删除任务
python3 main.py complete 1
python3 main.py delete 1

# 指定独立的数据文件
python3 main.py --data-file /tmp/demo-tasks.json list
```

任务默认保存在项目根目录的 `.taskflow.json`，该文件已被 Git 忽略。

## 运行测试

项目要求 Python 3.10 或更高版本，不依赖第三方运行库。

```bash
python3 -m unittest discover -s tests -v
```

Pull Request 和推送到核心分支时，[GitHub Actions](.github/workflows/tests.yml)
也会运行相同测试。

## 分支模型

| 分支 | 创建自 | 合并到 | 用途 |
| --- | --- | --- | --- |
| `main` | — | — | 保存已发布、可部署代码 |
| `develop` | `main` | `main` | 集成下一版本的功能 |
| `feature/*` | `develop` | `develop` | 开发独立功能 |
| `bugfix/*` | `develop` | `develop` | 修复尚未发布的问题 |
| `release/*` | `develop` | `main`、`develop` | 发布前稳定版本 |
| `hotfix/*` | `main` | `main`、`develop` | 紧急修复生产问题 |

本教学仓库保留了已合并的短期分支，便于查看分支指针。真实项目通常会在 PR
合并后删除 `feature/*`、`bugfix/*`、`release/*` 和 `hotfix/*` 分支。

## 一次功能开发

```bash
git switch develop
git pull
git switch -c feature/example

# 编码并小步提交
git add .
git commit -m "feat: add example command"

# 推送后创建 Pull Request，请求合并到 develop
git push -u origin feature/example
```

合并前应确保测试通过，并同步最新的 `develop`。本仓库中的
`feature/add-task` 与 `feature/list-tasks` 从同一个提交并行开发，合并第二个
分支时真实产生过冲突，合并提交展示了同时保留两项业务能力的解决结果。

## 一次正式发布

```bash
git switch develop
git switch -c release/1.0.0

# 仅允许修复发布阻塞问题、更新版本和文档
git switch main
git merge --no-ff release/1.0.0
git tag -a v1.0.0 -m "release: v1.0.0"

# 将发布阶段的修改同步回开发线
git switch develop
git merge --no-ff release/1.0.0
```

## 一次生产热修复

```bash
git switch main
git switch -c hotfix/example

# 修复、测试、提交后发布补丁版本
git switch main
git merge --no-ff hotfix/example
git tag -a v1.0.1 -m "release: v1.0.1"

# 必须回灌，避免后续版本重新引入相同问题
git switch develop
git merge --no-ff hotfix/example
```

## 提交和 Pull Request

提交信息使用 Conventional Commits：

```text
feat: add task completion command
fix: reject blank task titles
test: cover missing task behavior
docs: explain release workflow
chore: prepare 1.0.0 release
```

一个 Pull Request 应只解决一个主题，并包含变更说明、验证方法和风险。推荐为
`main` 与 `develop` 开启分支保护，禁止直接推送，并要求测试通过和至少一人审查。

## 查看教学历史

```bash
git log --graph --decorate --oneline --all
git show feature/add-task
git show feature/list-tasks
git show v1.0.0
git diff v1.0.0..v1.0.1
```

建议按根提交到最新标签的顺序阅读，观察功能分支如何汇入 `develop`、发布分支
如何进入 `main`，以及热修复为何需要同时同步两条长期分支。
