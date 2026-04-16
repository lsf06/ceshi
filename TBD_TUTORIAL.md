# Trunk-Based Development (TBD) 实战教程

## 核心概念

### TBD vs GitFlow 对比

| 特性 | TBD (主干开发) | GitFlow |
|------|---------------|---------|
| **主分支** | 只有 main | main + develop + release + hotfix |
| **分支寿命** | < 8 小时 | 数天到数周 |
| **合并频率** | 每天多次 | 每周/每月 |
| **功能开关** | Feature Flags 必需 | 可选 |
| **部署状态** | main 永远可部署 | develop 可能不稳定 |
| **适用场景** | CI/CD、敏捷团队 | 版本发布周期长的项目 |

### TBD 核心规则

```
┌─────────────────────────────────────────────────────────────┐
│                    TBD 核心规则                               │
├─────────────────────────────────────────────────────────────┤
│  ✅ 几乎只用 main 分支                                        │
│  ✅ 分支寿命 < 8 小时                                         │
│  ✅ 每次合并前必须通过测试                                    │
│  ✅ 使用 Feature Flags 控制未完成功能                         │
│  ✅ 每天多次小合并                                            │
│  ❌ 禁止长期存在的 feature 分支                               │
│  ❌ 禁止绕过代码审查                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Feature Flag 实现

### Python Feature Flag 示例

```python
# src/ml/config.py

import os

class Config:
    """配置管理 - 使用 Feature Flags 控制功能"""
    
    # === Feature Flags ===
    USE_NEW_MODEL = os.getenv("USE_NEW_MODEL", "false").lower() == "true"
    USE_ENHANCED_PREPROCESSING = os.getenv("USE_ENHANCED_PREPROCESSING", "false").lower() == "true"
    USE_ADVANCED_AUGMENTATION = os.getenv("USE_ADVANCED_AUGMENTATION", "false").lower() == "true"
    
    # === 基础配置 ===
    MODEL_PATH = "models/model.onnx"
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    
    @classmethod
    def get_model_config(cls):
        """根据 Feature Flag 返回模型配置"""
        if cls.USE_NEW_MODEL:
            return {
                "type": "transformer_v2",
                "d_model": 128,
                "nhead": 8,
                "num_layers": 4,
                "enabled": True
            }
        else:
            return {
                "type": "transformer_v1",
                "d_model": 64,
                "nhead": 4,
                "num_layers": 2,
                "enabled": True
            }
    
    @classmethod
    def get_preprocessing_config(cls):
        """根据 Feature Flag 返回预处理配置"""
        if cls.USE_ENHANCED_PREPROCESSING:
            return {
                "normalize": True,
                "augment": cls.USE_ADVANCED_AUGMENTATION,
                "dropout": 0.3
            }
        else:
            return {
                "normalize": False,
                "augment": False,
                "dropout": 0.0
            }
```

### 使用 Feature Flag 的训练代码

```python
# src/ml/train.py

import os
from config import Config

def train():
    """模型训练入口 - 使用 Feature Flags"""
    
    print("=" * 50)
    print("模型训练启动")
    print("=" * 50)
    
    # 显示当前 Feature Flag 状态
    print("\n[Feature Flags]")
    print(f"  USE_NEW_MODEL: {Config.USE_NEW_MODEL}")
    print(f"  USE_ENHANCED_PREPROCESSING: {Config.USE_ENHANCED_PREPROCESSING}")
    print(f"  USE_ADVANCED_AUGMENTATION: {Config.USE_ADVANCED_AUGMENTATION}")
    
    # 获取模型配置
    model_config = Config.get_model_config()
    print(f"\n[模型配置]")
    print(f"  类型：{model_config['type']}")
    print(f"  d_model: {model_config['d_model']}")
    
    # 根据 Feature Flag 选择训练逻辑
    if Config.USE_NEW_MODEL:
        print("\n[训练] 使用 Transformer v2 模型...")
        # 新模型训练逻辑
        result = train_transformer_v2()
    else:
        print("\n[训练] 使用 Transformer v1 模型...")
        # 旧模型训练逻辑（稳定版本）
        result = train_transformer_v1()
    
    print(f"\n[结果] 训练完成，准确率：{result['accuracy']:.2%}")
    return result

def train_transformer_v1():
    """稳定的 v1 模型训练"""
    return {"accuracy": 0.85, "version": "v1"}

def train_transformer_v2():
    """实验性的 v2 模型训练"""
    # 这里可能还不稳定，但通过 Feature Flag 可以控制
    return {"accuracy": 0.92, "version": "v2"}

if __name__ == "__main__":
    train()
```

---

## Git 操作流程

### 完整的 TBD 工作流命令

```bash
# ============================================
# 步骤 1: 同步 main 分支
# ============================================
git checkout main
git pull origin main

# ============================================
# 步骤 2: 创建短期 feature 分支（寿命 < 8 小时）
# ============================================
git checkout -b feature/tune-lr-20240416

# ============================================
# 步骤 3: 开发功能（使用 Feature Flag 保护）
# ============================================
# 修改代码，确保新功能被 Feature Flag 保护
# vim src/ml/config.py
# 添加：NEW_LEARNING_RATE = os.getenv("NEW_LEARNING_RATE", "false") == "true"

# ============================================
# 步骤 4: 提交代码
# ============================================
git add .
git commit -m "feat: 添加新的学习率调度器 [WIP]"

# ============================================
# 步骤 5: 推送分支
# ============================================
git push -u origin feature/tune-lr-20240416

# ============================================
# 步骤 6: 创建 PR/MR（在 GitHub/GitLab 网页端）
# ============================================
# 创建 Pull Request，等待 CI 测试通过

# ============================================
# 步骤 7: 本地测试（合并前）
# ============================================
git checkout main
git pull origin main
git merge feature/tune-lr-20240416
python -m pytest tests/

# ============================================
# 步骤 8: 合并到 main（在 PR 通过后）
# ============================================
# 在 GitHub/GitLab 网页端点击 "Merge"

# ============================================
# 步骤 9: 同步本地 main
# ============================================
git checkout main
git pull origin main

# ============================================
# 步骤 10: 删除远程和本地 feature 分支
# ============================================
git branch -d feature/tune-lr-20240416
git push origin --delete feature/tune-lr-20240416
```

---

## 练习：3 次模型调参循环

### 循环 1: 调整学习率

```bash
# 1. 同步 main
git checkout main
git pull origin main

# 2. 创建短期分支
git checkout -b feature/tune-lr-v1

# 3. 修改配置（使用 Feature Flag）
# 在 config.py 中添加新的学习率配置

# 4. 提交
git add .
git commit -m "feat: 添加可配置学习率 [FEATURE_FLAG]"

# 5. 推送
git push -u origin feature/tune-lr-v1

# 6. 等待 PR 通过后合并
# (在 GitHub 网页端完成)

# 7. 同步
git checkout main
git pull origin main
```

### 循环 2: 调整批次大小

```bash
# 1. 创建新分支
git checkout -b feature/tune-batch-size

# 2. 修改配置
# 添加批次大小 Feature Flag

# 3. 提交并推送
git add .
git commit -m "feat: 添加批次大小调优 [FEATURE_FLAG]"
git push -u origin feature/tune-batch-size

# 4. 等待 PR 通过后合并
# (在 GitHub 网页端完成)

# 5. 同步
git checkout main
git pull origin main
```

### 循环 3: 调整模型层数

```bash
# 1. 创建新分支
git checkout -b feature/tune-layers

# 2. 修改配置
# 添加模型层数 Feature Flag

# 3. 提交并推送
git add .
git commit -m "feat: 添加模型层数调优 [FEATURE_FLAG]"
git push -u origin feature/tune-layers

# 4. 等待 PR 通过后合并
# (在 GitHub 网页端完成)

# 5. 同步
git checkout main
git pull origin main
```

---

## Feature Flag 在 AI 项目的优势

### 1. 安全实验
```python
# 新模型还在实验中，但不影响主流程
if Config.USE_EXPERIMENTAL_MODEL:
    # 实验代码，可能不稳定
    model = ExperimentalModel()
else:
    # 稳定代码，保证服务可用
    model = StableModel()
```

### 2. 快速回滚
```bash
# 不需要回滚代码，只需关闭 Feature Flag
export USE_NEW_MODEL=false
python train.py  # 立即切回旧模型
```

### 3. A/B 测试
```python
# 按比例流量测试
import random
if random.random() < 0.1 and Config.USE_NEW_MODEL:
    # 10% 流量使用新模型
    return train_new_model()
else:
    # 90% 流量使用旧模型
    return train_old_model()
```

### 4. 持续集成
- 代码随时在 main 分支，保持可测试
- 新功能通过 Flag 控制，不影响现有功能
- 每天多次合并，减少合并冲突

---

## 分支生命周期图

```
main ──┬── feature/xxx (2 小时) ──→ PR ──→ main
       ├── feature/yyy (4 小时) ──→ PR ──→ main
       └── feature/zzz (6 小时) ──→ PR ──→ main

每个分支独立开发，快速合并，main 始终绿色
```

---

## 检查清单

每次开发前确认：

- [ ] 当前在 main 分支
- [ ] main 已同步最新代码
- [ ] 分支命名清晰（feature/描述 - 日期）
- [ ] 新功能有 Feature Flag 保护
- [ ] 本地测试通过
- [ ] PR 描述清晰
- [ ] CI 测试通过
- [ ] 代码审查通过
- [ ] 合并后删除分支