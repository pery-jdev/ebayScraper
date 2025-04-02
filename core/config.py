from pathlib import Path
import yaml
import os

class Config:
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.config = self._load_config()
        
        
    def _load_config(self):
    # Load base config
        base_path = self.BASE_DIR / 'config' / 'base.yaml'
        with open(base_path) as f:
            config = yaml.safe_load(f)
            
        # Load environment specific config
        env = os.getenv('APP_ENV', 'development')
        env_path = self.BASE_DIR / 'config' / f'{env}.yaml'
        
        # Special handling for testing environment
        if env == 'testing':
            env_path = self.BASE_DIR / 'tests' / 'fixtures' / 'test_config.yaml'
            
        if env_path.exists():
            with open(env_path) as f:
                env_config = yaml.safe_load(f)
                config = self._merge_configs(config, env_config)
                
        # Set directories
        self.TEMP_DIR = self.BASE_DIR / config['base']['directories']['temp']
        self.DATA_DIR = self.BASE_DIR / config['base']['directories']['data']
        self.DRIVER_PATH = self.TEMP_DIR / config['base']['directories']['driver']
        
        # Set debug mode
        self.DEBUG = config['base']['debug']
        
        # Set translation config
        self.TRANSLATION = config['translation']
        
        # Set currency config
        self.ALPHA_VANTAGE_KEY = config['currency']['alphavantage_api_key']
        
        return config

    def _merge_configs(self, base, override):
        """Deep merge two config dictionaries"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._merge_configs(base[key], value)
            else:
                base[key] = value
        return base

    def get(self, key, default=None):
        """Get config value using dot notation"""
        keys = key.split('.')
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

# Singleton instance
config = Config()