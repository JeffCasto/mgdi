# Local model provider stub
from .base import BaseModelProvider

class LocalProvider(BaseModelProvider):
    def generate(self, prompt, **kwargs):
        return 'Local model response'
