# CI/CD 配置指南

本项目使用 GitHub Actions 实现自动化的持续集成和持续部署。

## 1. 流程概览

### CI (持续集成)
- **触发条件**: 推送到 `main` 或 `dev` 分支，以及针对这些分支的 Pull Request。
- **执行步骤**:
  1.  检出代码。
  2.  安装 Python 环境 (3.10, 3.11, 3.12)。
  3.  安装依赖 (`requirements.txt`)。
  4.  运行代码风格检查 (`flake8`)。
  5.  运行单元测试 (`pytest`)。
  6.  构建 Docker 镜像 (确保构建成功，不推送)。

### CD (持续部署)
- **触发条件**: 推送标签 (Tag) 匹配 `v*` (例如 `v1.0.0`)。
- **执行步骤**:
  1.  构建 Docker 镜像并推送到 Docker Hub。
  2.  通过 SSH 连接到生产服务器。
  3.  拉取最新镜像。
  4.  停止并移除旧容器。
  5.  启动新容器。

## 2. 配置 Secrets

要在 GitHub 上启用部署功能，需要在仓库设置 (Settings -> Secrets and variables -> Actions) 中配置以下 Secrets：

### Docker Hub 配置
| Secret 名称 | 描述 |
| --- | --- |
| `DOCKERHUB_USERNAME` | Docker Hub 用户名 |
| `DOCKERHUB_TOKEN` | Docker Hub Access Token (推荐) 或密码 |

### 生产环境服务器配置 (CD 需要)
| Secret 名称 | 描述 |
| --- | --- |
| `PROD_HOST` | 生产服务器 IP 地址 |
| `PROD_USERNAME` | SSH 用户名 |
| `PROD_SSH_KEY` | SSH 私钥 (PEM 格式) |

### 数据库配置 (用于运行时注入)
| Secret 名称 | 描述 |
| --- | --- |
| `DB_HOST` | MySQL 数据库主机 |
| `DB_USER` | 数据库用户名 |
| `DB_PASSWORD` | 数据库密码 |
| `DB_NAME` | 数据库名称 |

## 3. 如何发布新版本

1.  确保代码在 `main` 分支上，且 CI 通过。
2.  打上版本标签并推送：

```bash
git tag v1.0.0
git push origin v1.0.0
```

这将自动触发 CD 流程，构建镜像并部署到生产环境。

## 4. 本地测试

在提交前，建议在本地运行测试：

```bash
# 安装测试依赖
pip install pytest flake8

# 运行测试
pytest

# 运行 Lint 检查
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```
