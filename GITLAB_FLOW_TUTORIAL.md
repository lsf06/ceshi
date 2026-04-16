# GitLab Flow 实战教程 - AI/硬件项目全流程

## 分支策略概览

```
                    ┌─────────┐
                    │ develop │ ← 开发分支（日常开发）
                    └────┬────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌────────┐      ┌────────┐      ┌────────────┐
   │feature │      │  hotfix│      │release/v1  │
   └────────┘      └────────┘      └────────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   ┌────────┐      ┌────────┐      ┌────────────┐
   │staging │      │production│    │  main      │
   │(测试)  │      │  (生产)  │    │ (主分支)   │
   └────────┘      └────────┘      └────────────┘
```

---

## 环境分支定义

| 分支 | 用途 | 更新方式 |
|------|------|----------|
| `main` | 主分支，所有代码的源头 | 从 develop 定期合并 |
| `develop` | 开发分支，日常开发 | 功能分支合并至此 |
| `staging` | 预发布/测试环境 | 从 release 分支创建 |
| `production` | 生产环境 | 从 staging 审批后创建 |

---

## 全流程操作指南

### 步骤 1: 切换到 main 并同步最新代码

```bash
# 切换到 main 分支
git checkout main

# 拉取远程最新代码
git pull origin main

# 确认工作区干净
git status
# 输出应为：nothing to commit, working tree clean
```

**原理**：所有新环境分支都应该基于最新的 main 创建，确保基线一致。

---

### 步骤 2: 创建 develop 开发分支（如不存在）

```bash
# 从 main 创建 develop 分支
git checkout -b develop

# 推送到远程
git push -u origin develop
```

---

### 步骤 3: 在 develop 上开发新功能

```bash
# 切换到 develop
git checkout develop

# 创建功能分支
git checkout -b feature/model-v2

# 修改代码（例如升级模型）
# vim src/ml/train.py

# 提交并推送
git add .
git commit -m "feat: 升级模型到 v2 版本"
git push -u origin feature/model-v2
```

---

### 步骤 4: 合并功能到 develop

```bash
# 切换回 develop
git checkout develop

# 拉取最新
git pull origin develop

# 合并功能分支
git merge feature/model-v2

# 推送 develop
git push origin develop
```

---

### 步骤 5: 创建 release 分支并部署到 staging

```bash
# 从 develop 创建 release 分支
git checkout -b release/v1.0 develop

# 推送 release 分支
git push -u origin release/v1.0

# 创建 staging 环境分支
git checkout -b staging release/v1.0

# 推送 staging
git push -u origin staging
```

**Staging 环境说明**：
- 用于模型测试和硬件验证
- 自动化 CI/CD 触发测试
- 测试通过后才能进入 production

---

### 步骤 6: 在 staging 环境进行模型测试

```bash
# 切换到 staging
git checkout staging

# 拉取模型数据（DVC）
dvc pull models/model.onnx

# 运行测试
python -m pytest tests/

# 验证硬件固件
# 运行仿真测试
```

---

### 步骤 7: 硬件验证阶段

```bash
# 创建硬件验证分支
git checkout -b hw-verification staging

# 添加硬件测试配置
# vim .gitlab-ci.yml

# 提交验证结果
git add .
git commit -m "test: 硬件验证通过"
git push -u origin hw-verification

# 合并回 staging
git checkout staging
git merge hw-verification
git push origin staging
```

---

### 步骤 8: 部署到 production（需审批）

```bash
# 从 staging 创建 production 分支
git checkout -b production staging

# 推送 production
git push -u origin production

# 标记发布版本
git tag -a v1.0.0 -m "Release v1.0.0 to production"
git push origin v1.0.0
```

---

## AI 硬件专属规则

### ⚠️ Production 分支保护规则

```
┌─────────────────────────────────────────────────────────┐
│  Production 分支操作限制                                  │
├─────────────────────────────────────────────────────────┤
│  ✅ 允许：hotfix 分支合并（紧急修复）                     │
│  ❌ 禁止：feature/release 分支直接合并                   │
│  ❌ 禁止：直接 push 到 production                        │
│  ✅ 必须：代码审查 + 审批流程                            │
└─────────────────────────────────────────────────────────┘
```

### Hotfix 分支操作流程

```bash
# 1. 从 production 创建 hotfix
git checkout -b hotfix/production-issue production

# 2. 修复问题
# vim src/ml/train.py

# 3. 提交修复
git add .
git commit -m "fix: 修复生产环境模型加载问题"

# 4. 推送到远程
git push -u origin hotfix/production-issue

# 5. 在 GitLab 创建 MR 到 production（需审批）

# 6. 审批通过后合并
git checkout production
git merge hotfix/production-issue

# 7. 同步到 main 和 develop
git checkout main
git merge production
git push origin main

git checkout develop
git merge production
git push origin develop
```

---

## GitLab CI/CD 流水线配置

### .gitlab-ci.yml 完整配置

```yaml
# .gitlab-ci.yml

stages:
  - test
  - build
  - deploy-staging
  - deploy-production

# 变量定义
variables:
  PYTHON_VERSION: "3.10"
  DVC_REMOTE: "s3://my-bucket/dvc-cache"

# 通用测试模板
.test_template: &test_template
  stage: test
  script:
    - pip install -r requirements.txt
    - dvc pull
    - python -m pytest tests/ -v
    - python -m pytest tests/verilog/ -v  # 硬件测试

# 开发分支测试
test-develop:
  <<: *test_template
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

# Staging 环境部署
deploy-staging:
  stage: deploy-staging
  script:
    - echo "Deploying to staging environment..."
    - dvc pull models/
    - python src/ml/evaluate.py
    - ./scripts/verify_hardware.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "staging"
  environment:
    name: staging
    url: https://staging.example.com

# 硬件验证（仅在 staging）
hardware-verification:
  stage: build
  script:
    - echo "Running hardware verification..."
    - iverilog -o test_top tests/verilog/test_firmware.v hw/verilog/firmware.v
    - vvp test_top
  rules:
    - if: $CI_COMMIT_BRANCH == "staging"
  dependencies:
    - deploy-staging

# Production 部署（需要手动审批）
deploy-production:
  stage: deploy-production
  script:
    - echo "Deploying to production environment..."
    - dvc pull models/
    - ./scripts/deploy_production.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "production"
  when: manual  # 需要手动触发
  environment:
    name: production
    url: https://example.com
  variables:
    DEPLOY_ENV: "production"
```

---

## CI/CD 触发条件说明

| 分支 | 触发动作 | 自动化测试 | 硬件验证 | 部署 |
|------|----------|------------|----------|------|
| `develop` | 每次 push | ✅ | ❌ | ❌ |
| `staging` | 每次 push | ✅ | ✅ | ✅ (自动) |
| `production` | 每次 push | ✅ | ✅ | ⚠️ (需审批) |
| `hotfix/*` | 每次 push | ✅ | ✅ | ⚠️ (需审批) |

---

## 完整流程总结

```
┌────────────────────────────────────────────────────────────────┐
│                     GitLab Flow 完整流程                        │
└────────────────────────────────────────────────────────────────┘

1. 开发阶段
   main ──→ develop ──→ feature/* ──→ develop
   
2. 测试阶段
   develop ──→ release/v1.0 ──→ staging
                                    │
                                    ▼
                            自动化测试 + 硬件验证
   
3. 生产阶段
   staging ──→ production (需审批)
                │
                ▼
          标记版本标签 v1.0.0
   
4. 紧急修复
   production ──→ hotfix/* ──→ production
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
                   main    develop   staging
```

---

## 常用命令速查

```bash
# 环境分支管理
git checkout -b staging develop      # 创建 staging
git checkout -b production staging   # 创建 production
git checkout -b hotfix/xxx production # 创建 hotfix

# 分支同步
git checkout main && git merge production
git checkout develop && git merge production

# 版本标签
git tag -a v1.0.0 -m "Release note"
git push origin v1.0.0

# 查看环境状态
git branch -a                      # 查看所有分支
git log --oneline staging..production  # 查看 staging 到 production 的差异