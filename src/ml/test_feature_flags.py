"""
Feature Flag 测试脚本 - 不依赖外部库
"""

import os
import sys

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config


def test_default_config():
    """测试默认配置（所有 Feature Flag 关闭）"""
    print("\n" + "=" * 60)
    print("测试 1: 默认配置 (所有 Feature Flag 关闭)")
    print("=" * 60)
    
    Config.print_config_status()
    
    model_config = Config.get_model_config()
    assert model_config["type"] == "transformer_v1", "默认应该使用 v1 模型"
    assert model_config["num_layers"] == 2, "默认应该是 2 层"
    print("✓ 默认配置测试通过")


def test_new_model_flag():
    """测试 USE_NEW_MODEL 标志"""
    print("\n" + "=" * 60)
    print("测试 2: 启用 USE_NEW_MODEL")
    print("=" * 60)
    
    os.environ["USE_NEW_MODEL"] = "true"
    # 重新导入以读取新环境变量
    import importlib
    import config
    importlib.reload(config)
    
    config.Config.print_config_status()
    
    model_config = config.Config.get_model_config()
    assert model_config["type"] == "transformer_v2", "应该使用 v2 模型"
    assert model_config["num_layers"] == 4, "v2 应该是 4 层"
    print("✓ USE_NEW_MODEL 测试通过")


def test_deeper_model_flag():
    """测试 USE_DEEPER_MODEL 标志"""
    print("\n" + "=" * 60)
    print("测试 3: 启用 USE_DEEPER_MODEL")
    print("=" * 60)
    
    os.environ["USE_DEEPER_MODEL"] = "true"
    os.environ["USE_NEW_MODEL"] = "false"  # 确保另一个 Flag 关闭
    
    import importlib
    import config
    importlib.reload(config)
    
    config.Config.print_config_status()
    
    model_config = config.Config.get_model_config()
    assert model_config["type"] == "transformer_deep", "应该使用 deep 模型"
    assert model_config["num_layers"] == 6, "deep 应该是 6 层"
    assert model_config["d_model"] == 256, "deep 应该是 256 维"
    print("✓ USE_DEEPER_MODEL 测试通过")


def test_learning_rate_scheduler_flag():
    """测试学习率调度器 Flag"""
    print("\n" + "=" * 60)
    print("测试 4: 启用 USE_NEW_LEARNING_RATE_SCHEDULER")
    print("=" * 60)
    
    os.environ["USE_NEW_LEARNING_RATE_SCHEDULER"] = "true"
    
    import importlib
    import config
    importlib.reload(config)
    
    config.Config.print_config_status()
    
    train_config = config.Config.get_training_config()
    assert train_config["lr_scheduler"]["type"] == "cosine_annealing", "应该使用余弦调度"
    print("✓ 学习率调度器测试通过")


def test_batch_size_flag():
    """测试批次大小 Flag"""
    print("\n" + "=" * 60)
    print("测试 5: 启用 USE_ENHANCED_BATCH_SIZE")
    print("=" * 60)
    
    os.environ["USE_ENHANCED_BATCH_SIZE"] = "true"
    
    import importlib
    import config
    importlib.reload(config)
    
    config.Config.print_config_status()
    
    train_config = config.Config.get_training_config()
    assert train_config["batch_size"] == 128, "批次大小应该是 128"
    print("✓ 批次大小测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "#" * 60)
    print("# Feature Flag 测试套件")
    print("#" * 60)
    
    try:
        test_default_config()
    except Exception as e:
        print(f"✗ 默认配置测试失败：{e}")
    
    try:
        test_new_model_flag()
    except Exception as e:
        print(f"✗ USE_NEW_MODEL 测试失败：{e}")
    
    try:
        test_deeper_model_flag()
    except Exception as e:
        print(f"✗ USE_DEEPER_MODEL 测试失败：{e}")
    
    try:
        test_learning_rate_scheduler_flag()
    except Exception as e:
        print(f"✗ 学习率调度器测试失败：{e}")
    
    try:
        test_batch_size_flag()
    except Exception as e:
        print(f"✗ 批次大小测试失败：{e}")
    
    print("\n" + "#" * 60)
    print("# 所有测试完成")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    run_all_tests()