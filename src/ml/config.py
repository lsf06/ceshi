"""
配置管理 - 使用 Feature Flags 控制功能
"""

import os


class Config:
    """配置类 - 所有 Feature Flags 集中管理"""
    
    # ==================== Feature Flags ====================
    # 控制新模型功能的开关，默认关闭以保证稳定性
    
    USE_NEW_MODEL = os.getenv("USE_NEW_MODEL", "false").lower() == "true"
    USE_ENHANCED_PREPROCESSING = os.getenv("USE_ENHANCED_PREPROCESSING", "false").lower() == "true"
    USE_ADVANCED_AUGMENTATION = os.getenv("USE_ADVANCED_AUGMENTATION", "false").lower() == "true"
    USE_NEW_LEARNING_RATE_SCHEDULER = os.getenv("USE_NEW_LEARNING_RATE_SCHEDULER", "false").lower() == "true"
    USE_ENHANCED_BATCH_SIZE = os.getenv("USE_ENHANCED_BATCH_SIZE", "false").lower() == "true"
    USE_DEEPER_MODEL = os.getenv("USE_DEEPER_MODEL", "false").lower() == "true"
    
    # ==================== 基础配置 ====================
    MODEL_PATH = "models/model.onnx"
    DEFAULT_BATCH_SIZE = 32
    DEFAULT_LEARNING_RATE = 0.001
    DEFAULT_EPOCHS = 100
    
    # ==================== 模型配置 ====================
    
    @classmethod
    def get_model_config(cls):
        """根据 Feature Flag 返回模型配置"""
        if cls.USE_DEEPER_MODEL:
            return {
                "type": "transformer_deep",
                "d_model": 256,
                "nhead": 8,
                "num_layers": 6,
                "dropout": 0.3,
                "enabled": True
            }
        elif cls.USE_NEW_MODEL:
            return {
                "type": "transformer_v2",
                "d_model": 128,
                "nhead": 8,
                "num_layers": 4,
                "dropout": 0.2,
                "enabled": True
            }
        else:
            # 默认使用稳定的 v1 模型
            return {
                "type": "transformer_v1",
                "d_model": 64,
                "nhead": 4,
                "num_layers": 2,
                "dropout": 0.1,
                "enabled": True
            }
    
    # ==================== 预处理配置 ====================
    
    @classmethod
    def get_preprocessing_config(cls):
        """根据 Feature Flag 返回预处理配置"""
        if cls.USE_ENHANCED_PREPROCESSING:
            return {
                "normalize": True,
                "augment": cls.USE_ADVANCED_AUGMENTATION,
                "dropout": 0.3,
                "data_augmentation": {
                    "rotation": True,
                    "flip": True,
                    "zoom": True
                } if cls.USE_ADVANCED_AUGMENTATION else {}
            }
        else:
            return {
                "normalize": False,
                "augment": False,
                "dropout": 0.0,
                "data_augmentation": {}
            }
    
    # ==================== 训练配置 ====================
    
    @classmethod
    def get_training_config(cls):
        """根据 Feature Flag 返回训练配置"""
        batch_size = 128 if cls.USE_ENHANCED_BATCH_SIZE else cls.DEFAULT_BATCH_SIZE
        
        if cls.USE_NEW_LEARNING_RATE_SCHEDULER:
            lr_scheduler = {
                "type": "cosine_annealing",
                "T_max": 50,
                "eta_min": 1e-6
            }
        else:
            lr_scheduler = {
                "type": "step",
                "step_size": 30,
                "gamma": 0.1
            }
        
        return {
            "batch_size": batch_size,
            "learning_rate": cls.DEFAULT_LEARNING_RATE,
            "epochs": cls.DEFAULT_EPOCHS,
            "lr_scheduler": lr_scheduler
        }
    
    # ==================== 打印配置状态 ====================
    
    @classmethod
    def print_config_status(cls):
        """打印当前所有 Feature Flag 状态"""
        print("\n" + "=" * 50)
        print("配置状态")
        print("=" * 50)
        print("\n[Feature Flags]")
        print(f"  USE_NEW_MODEL: {cls.USE_NEW_MODEL}")
        print(f"  USE_ENHANCED_PREPROCESSING: {cls.USE_ENHANCED_PREPROCESSING}")
        print(f"  USE_ADVANCED_AUGMENTATION: {cls.USE_ADVANCED_AUGMENTATION}")
        print(f"  USE_NEW_LEARNING_RATE_SCHEDULER: {cls.USE_NEW_LEARNING_RATE_SCHEDULER}")
        print(f"  USE_ENHANCED_BATCH_SIZE: {cls.USE_ENHANCED_BATCH_SIZE}")
        print(f"  USE_DEEPER_MODEL: {cls.USE_DEEPER_MODEL}")
        
        print("\n[模型配置]")
        model_config = cls.get_model_config()
        for key, value in model_config.items():
            print(f"  {key}: {value}")
        
        print("\n[训练配置]")
        train_config = cls.get_training_config()
        for key, value in train_config.items():
            print(f"  {key}: {value}")
        
        print("=" * 50 + "\n")