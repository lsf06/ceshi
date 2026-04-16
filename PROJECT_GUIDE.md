# EdgeAI Robot 项目使用指南

## 一、Monorepo 架构优势

### 什么是 Monorepo？
Monorepo（单一代码库）是将多个相关项目的所有代码、配置和文件放在同一个版本控制仓库中的开发模式。

### 核心优势

| 优势 | 说明 |
|------|------|
| **统一管理** | 所有代码在一个仓库，便于版本控制和依赖管理 |
| **跨团队协作** | 软件、硬件、算法团队在同一代码库协作 |
| **原子提交** | 跨模块的修改可以一次性提交，保持一致性 |
| **简化 CI/CD** | 统一的构建和部署流程，减少配置复杂度 |
| **代码复用** | 模块间共享代码更容易，避免重复实现 |

### 本项目结构
```
edge-ai-robot-practice/
├── src/              # 源代码
│   ├── ml/          # 机器学习训练代码
│   └── inference/   # 推理部署代码
├── hw/              # 硬件相关
│   ├── verilog      # Verilog 代码
│   └── pcb          # PCB 设计文件
├── data/            # 数据集
├── models/          # 模型文件
├── experiments/     # 实验记录
├── tests/           # 测试代码
└── .github/         # CI/CD配置
```

---

## 二、DVC 如何管理大文件

### DVC 是什么？
DVC (Data Version Control) 是一个开源的数据版本控制系统，专为机器学习项目设计。

### 核心功能

1. **数据版本控制**
   - 类似 Git，但专为大文件优化
   - 不将大文件存入 Git，只存指针文件
   - 支持数据文件的版本管理和回滚

2. **远程存储**
   - 大文件存储在云存储（S3、GCS、Azure 等）或 NFS
   - Git 只保存轻量级指针文件（.dvc 文件）

3. **实验追踪**
   - 记录每次实验的参数、指标和输出
   - 可复现历史实验结果

### 基本使用命令

```bash
# 初始化 DVC（已完成）
dvc init

# 添加大文件到 DVC 管理
dvc add data/dataset.csv
dvc add models/model.onnx

# 配置远程存储
dvc remote add myremote s3://my-bucket/path

# 推送到远程
dvc push

# 从远程拉取
dvc pull

# 运行训练管道
dvc repro
```

### Git LFS vs DVC
| 特性 | Git LFS | DVC |
|------|---------|-----|
| 适用场景 | 二进制大文件 | 数据集、模型、实验 |
| 版本控制 | 支持 | 支持 + 实验追踪 |
| 远程存储 | 需 LFS 服务器 | 支持多种云存储 |
| 管道管理 | 不支持 | 支持 |

---

## 三、开发规范

### 3.1 添加代码文件

```bash
# Python 代码
mkdir -p src/ml
# 创建 src/ml/train.py，写入训练逻辑

# 提交代码
git add src/ml/train.py
git commit -m "feat: 添加模型训练脚本"
git push
```

### 3.2 添加模型文件

```bash
# 1. 将模型添加到 DVC 管理
dvc add models/model.onnx

# 2. 提交 DVC 指针文件
git add models/model.onnx.dvc models/.gitignore
git commit -m "feat: 添加训练好的模型"
git push

# 3. 团队成员拉取
dvc pull models/model.onnx
```

### 3.3 添加数据集

```bash
# 1. 添加原始数据（会被 .gitignore 忽略）
cp your_data.csv data/raw/

# 2. 添加处理后的数据到 DVC
dvc add data/processed/dataset.csv

# 3. 提交
git add data/processed/dataset.csv.dvc
git commit -m "data: 添加新数据集"
git push
```

### 3.4 添加硬件文件

```bash
# Verilog 代码直接提交
git add hw/verilog/*.v
git commit -m "feat: 添加 Verilog 模块"

# PCB 设计文件通过 Git LFS 管理
git lfs track "hw/pcb/*.sch"
git lfs track "hw/pcb/*.brd"
git add .gitattributes
git commit -m "chore: 配置 PCB 文件 LFS 跟踪"
```

---

## 四、环境安装命令

### Windows (PowerShell)
```powershell
# Git
winget install Git.Git

# Python
winget install Python.Python.3.12

# DVC
pip install dvc
pip install dvc-s3  # 如需 S3 支持
```

### Linux (Ubuntu/Debian)
```bash
# Git
sudo apt update && sudo apt install -y git

# Python
sudo apt install -y python3 python3-pip python3-venv

# DVC
pip3 install dvc
```

### macOS
```bash
# 使用 Homebrew
brew install git python3

# DVC
pip3 install dvc
```

---

## 五、快速开始

```bash
# 克隆项目
git clone https://github.com/lsf06/ceshi.git
cd ceshi

# 安装依赖
pip install -r requirements.txt

# 拉取数据
dvc pull

# 运行训练
python src/ml/train.py
```

---

## 六、常见问题

**Q: 推送时遇到 LFS 错误？**
A: 确保已安装 Git LFS：`git lfs install`

**Q: 拉取数据失败？**
A: 检查远程存储配置：`dvc remote list`

**Q: 如何查看数据版本历史？**
A: 使用 `dvc checkout <commit-hash>` 切换版本