# GitHub Flow 实操教程

## 前置说明：GitHub Flow 工作流程

```
main (生产分支)
   │
   ├─── feature/new-transformer-model (第一个功能分支)
   │
   └─── feature/hardware-firmware-v2 (第二个功能分支)
```

---

## 第一部分：开发第一个功能分支 - feature/new-transformer-model

### 步骤 1: 确保 main 分支是最新的
```bash
# 切换到 main 分支
git checkout main

# 拉取远程最新代码（防止本地落后）
git pull origin main
```
**原理说明**：
- `git checkout main`：切换到主分支，所有新功能都应该基于最新的 main 创建
- `git pull origin main`：同步远程仓库的最新变更，避免合并冲突

### 步骤 2: 创建新的 feature 分支
```bash
# 基于 main 创建新分支
git checkout -b feature/new-transformer-model
```
**原理说明**：
- `-b` 表示创建新分支并切换过去
- 分支命名规范 `feature/功能描述` 便于识别
- 每个功能独立开发，互不干扰

### 步骤 3: 修改训练代码（添加 Transformer 支持）
```bash
# 编辑训练文件
vim src/ml/train.py
```

将 `src/ml/train.py` 内容修改为：
```python
import torch
import torch.nn as nn

class TransformerModel(nn.Module):
    """简单的 Transformer 模型"""
    def __init__(self, input_dim, d_model=64, nhead=4, num_layers=2):
        super().__init__()
        self.embedding = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.classifier = nn.Linear(d_model, 2)
    
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        x = x.mean(dim=1)  # 池化
        return self.classifier(x)

def train():
    """模型训练入口"""
    print("开始训练 Transformer 模型...")
    
    # 创建模型
    model = TransformerModel(input_dim=10)
    print(f"模型参数数量：{sum(p.numel() for p in model.parameters())}")
    
    # TODO: 添加完整训练逻辑

if __name__ == "__main__":
    train()
```

### 步骤 4: 使用 DVC 追踪数据集
```bash
# 创建数据处理后的目录
mkdir -p data/processed

# 创建处理后的数据文件
echo "feature1,feature2,label,transformed
1.0,2.0,0,3.0
3.0,4.0,1,7.0" > data/processed/train.csv

# 用 DVC 追踪处理后的数据
dvc add data/processed/train.csv

# 查看生成的 DVC 文件
cat data/processed/train.csv.dvc
```
**DVC 原理说明**：
- `dvc add`：将文件添加到 DVC 管理，生成 `.dvc` 指针文件
- 原始大文件保存在 `.dvc/cache`，Git 只保存轻量级指针
- 团队成员拉取时，Git 拉取代码，DVC 拉取数据

### 步骤 5: 提交代码
```bash
# 添加所有变更
git add .

# 提交（遵循约定式提交规范）
git commit -m "feat: 添加 Transformer 模型训练支持

- 实现 TransformerModel 类
- 添加数据预处理流程
- 使用 DVC 追踪训练数据"
```

### 步骤 6: 推送到远程仓库
```bash
# 推送分支到远程
git push -u origin feature/new-transformer-model
```
**原理说明**：
- `-u` 设置上游分支，后续可直接用 `git push`
- 推送后可以在 GitHub 上创建 Pull Request

### 步骤 7: 在 GitHub 上创建 Pull Request
1. 访问 https://github.com/lsf06/ceshi.git
2. 点击 "Compare & pull request"
3. 填写 PR 描述，说明功能变更
4. 等待代码审查

### 步骤 8: 合并 PR 后，本地同步
```bash
# 切换回 main
git checkout main

# 拉取已合并的代码
git pull origin main
```

---

## 第二部分：开发第二个功能分支 - feature/hardware-firmware-v2

### 步骤 1: 基于最新的 main 创建分支
```bash
# 确保 main 最新
git checkout main
git pull origin main

# 创建硬件固件分支
git checkout -b feature/hardware-firmware-v2
```

### 步骤 2: 修改 Verilog 固件代码
```bash
# 编辑 Verilog 文件
vim hw/verilog/firmware.v
```

将 `hw/verilog/firmware.v` 内容修改为：
```verilog
`timescale 1ns/1ps

module top(
    input clk,
    input rst_n,
    input [7:0] data_in,
    input [3:0] op_code,
    output reg [7:0] data_out,
    output reg valid
);

// 操作码定义
`define ADD 4'b0000
`define SUB 4'b0001
`define MUL 4'b0010
`define DIV 4'b0011

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        data_out <= 8'd0;
        valid <= 1'b0;
    end else begin
        valid <= 1'b1;
        case (op_code)
            `ADD: data_out <= data_in + 8'd1;
            `SUB: data_out <= data_in - 8'd1;
            `MUL: data_out <= data_in * 2;
            `DIV: data_out <= data_in / 2;
            default: data_out <= data_in;
        endcase
    end
end

endmodule
```

### 步骤 3: 添加固件测试文件
```bash
# 创建测试目录
mkdir -p tests/verilog

# 创建测试文件
vim tests/verilog/test_firmware.v
```

```verilog
`timescale 1ns/1ps

module test_firmware;

reg clk;
reg rst_n;
reg [7:0] data_in;
reg [3:0] op_code;
wire [7:0] data_out;
wire valid;

// 实例化被测模块
top uut (
    .clk(clk),
    .rst_n(rst_n),
    .data_in(data_in),
    .op_code(op_code),
    .data_out(data_out),
    .valid(valid)
);

// 生成时钟
always #5 clk = ~clk;

initial begin
    clk = 0;
    rst_n = 0;
    data_in = 8'd0;
    op_code = 4'd0;
    
    // 复位
    #20 rst_n = 1;
    
    // 测试加法
    #10 op_code = `ADD; data_in = 8'd5;
    #10 data_in = 8'd10;
    
    // 测试乘法
    #10 op_code = `MUL; data_in = 8'd7;
    
    // 结束
    #20 $finish;
end

endmodule
```

### 步骤 4: 提交并推送
```bash
# 添加所有变更
git add .

# 提交
git commit -m "feat: 升级固件到 v2，支持多种运算

- 添加 ADD/SUB/MUL/DIV 操作
- 添加 Verilog 测试用例
- 改进代码结构"

# 推送
git push -u origin feature/hardware-firmware-v2
```

### 步骤 5: 创建 PR 并合并
（同步骤一，在 GitHub 上创建 PR 并合并）

### 步骤 6: 本地同步
```bash
git checkout main
git pull origin main
```

---

## 第三部分：查看提交历史

### 查看简略历史
```bash
# 查看最近 10 次提交
git log --oneline -10
```

### 查看图形化历史
```bash
# 查看分支合并图
git log --graph --oneline --all
```

### 查看 main 分支变更
```bash
# 对比当前 main 与初始提交
git log --oneline main
```

### 判断是否干净
```bash
# 查看工作区状态
git status

# 输出应为：
# On branch main
# Your branch is up to date with 'origin/main'.
# nothing to commit, working tree clean
```

**判断标准**：
- `nothing to commit, working tree clean`：工作区干净
- `Your branch is up to date with 'origin/main'`：与远程同步
- 提交历史包含预期的两个 feature 提交

---

## 第四部分：GitHub Flow 总结

### GitHub Flow 工作流程
```
1. 从 main 创建 feature 分支
2. 在分支上开发
3. 提交代码并推送到远程
4. 创建 Pull Request
5. 代码审查和讨论
6. 合并到 main
7. 部署到生产环境
```

### 优点

| 优点 | 说明 |
|------|------|
| **简单易懂** | 只有 main 和 feature 分支，流程清晰 |
| **持续集成** | 小步快跑，频繁合并，降低风险 |
| **代码审查** | PR 机制保证代码质量 |
| **功能隔离** | 每个功能独立开发，互不影响 |
| **快速回滚** | 问题出现时只需 revert 一次提交 |

### 缺点

| 缺点 | 说明 |
|------|------|
| **main 分支不稳定** | 合并前需确保 CI 通过 |
| **长周期功能困难** | 大功能需要拆分多个 PR |
| **合并冲突** | 多人并行开发易产生冲突 |
| **需要代码审查文化** | 团队需养成 Review 习惯 |

### AI 项目使用注意事项

1. **大文件管理**
   - 模型和数据用 DVC，不用 Git 直接提交
   - 配置 `.gitattributes` 自动处理 LFS 文件

2. **实验可复现**
   - 在 PR 描述中记录实验参数
   - 使用 DVC 追踪数据版本

3. **CI/CD 集成**
   - 配置 GitHub Actions 自动运行测试
   - 模型训练任务可用 DVC Pipeline

### 硬件项目使用注意事项

1. **设计文件管理**
   - Verilog/VHDL 代码用 Git 管理
   - PCB 二进制文件用 Git LFS

2. **版本兼容性**
   - 在 PR 中说明硬件版本
   - 固件和硬件版本需对应

3. **仿真验证**
   - 测试用例必须随代码提交
   - CI 中运行仿真验证

---

## 附录：常用 Git 命令速查

```bash
# 分支管理
git branch                    # 列出所有分支
git branch -a                 # 列出所有分支（含远程）
git checkout -b <name>        # 创建并切换
git checkout <name>           # 切换分支
git merge <name>              # 合并分支
git branch -d <name>          # 删除本地分支
git push origin --delete <name>  # 删除远程分支

# 同步代码
git pull                      # 拉取并合并
git fetch                     # 仅拉取不合并
git push                      # 推送

# 查看历史
git log                       # 查看历史
git log --oneline             # 简略视图
git log --graph               # 图形视图
git diff                      # 查看差异

# 暂存和恢复
git stash                     # 暂存当前工作
git stash pop                 # 恢复暂存
git reset HEAD                # 取消暂存区添加