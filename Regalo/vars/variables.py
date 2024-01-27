from typing import Any

class InstallerVars(dict):
    def __init__(self, *args, **kwargs):
        super(InstallerVars, self).__init__(*args, **kwargs)
    
    def __getattr__(self, key: str) -> Any:
        return self.get(key, None)