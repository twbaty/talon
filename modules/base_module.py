# recon_gui/modules/base_module.py

from abc import ABC, abstractmethod

class ReconModule(ABC):
    @abstractmethod
    def name(self) -> str:
        """Return the name of the module."""
        pass

    @abstractmethod
    def get_queries(self) -> dict:
        """Return a dictionary of predefined queries with parameterized templates."""
        pass

    @abstractmethod
    def render_query(self, template: str, params: dict) -> str:
        """Substitute params into the template and return the final query string."""
        pass

