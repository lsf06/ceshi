import torch
import torch.nn as nn
from config import Config


class TransformerModel(nn.Module):
    """Transformer 模型 - 支持多种配置"""
    
    def __init__(self, input_dim=10, config=None):
        super().__init__()
        
        if config is None:
            config = Config.get_model_config()
        
        self.config = config
        self.d_model = config["d_model"]
        
        self.embedding = nn.Linear(input_dim, self.d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=config["nhead"],
            dropout=config["dropout"]
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=config["num_layers"])
        self.classifier = nn.Linear(self.d_model, 2)
    
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        x = x.mean(dim=1)  # 池化
        return self.classifier(x)


def train():
    """模型训练入口 - 使用 Feature Flags"""
    
    # 打印当前配置状态
    Config.print_config_status()
    
    print("[训练] 开始训练...")
    
    # 根据 Feature Flag 选择模型配置
    model_config = Config.get_model_config()
    print(f"[模型] 使用 {model_config['type']}")
    
    # 创建模型
    model = TransformerModel(input_dim=10)
    param_count = sum(p.numel() for p in model.parameters())
    print(f"[模型] 参数数量：{param_count:,}")
    
    # 获取训练配置
    train_config = Config.get_training_config()
    print(f"[训练] 批次大小：{train_config['batch_size']}")
    print(f"[训练] 学习率调度器：{train_config['lr_scheduler']['type']}")
    
    # 模拟训练结果（根据配置返回不同准确率）
    result = simulate_training(model_config, train_config, param_count)
    
    print(f"\n[结果] 训练完成，准确率：{result['accuracy']:.2%}")
    print(f"[结果] 版本：{result['version']}")
    
    return result


def simulate_training(model_config, train_config, param_count):
    """模拟训练过程（实际使用时替换为真实训练）"""
    # 基础准确率
    base_accuracy = 0.85
    
    # 根据模型配置调整
    if model_config["type"] == "transformer_deep":
        base_accuracy = 0.93
    elif model_config["type"] == "transformer_v2":
        base_accuracy = 0.89
    
    # 根据训练配置调整
    if train_config["lr_scheduler"]["type"] == "cosine_annealing":
        base_accuracy += 0.02
    
    return {
        "accuracy": base_accuracy,
        "version": model_config["type"],
        "params": param_count
    }


if __name__ == "__main__":
    train()
