import os
import importlib.util
from .module_base import SwebModule

class ModuleManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.modules = []
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.modules_dir = os.path.join(self.base_dir, "modules")

    def load_all_modules(self):
        if not os.path.exists(self.modules_dir):
            os.makedirs(self.modules_dir)
            
        for filename in os.listdir(self.modules_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                filepath = os.path.join(self.modules_dir, filename)
                
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                
                for attr in dir(mod):
                    obj = getattr(mod, attr)
                    if isinstance(obj, type) and issubclass(obj, SwebModule) and obj is not SwebModule:
                        instance = obj(self.main_window)
                        self.modules.append(instance)
                        print(f"Module loaded successfully: {obj.__name__}")

    def get_all_actions(self):
        actions = []
        for module in self.modules:
            actions.extend(module.get_toolbar_actions())
        return actions