# recon_gui/modules/censys.py

from .base_module import ReconModule

class CensysModule(ReconModule):
    def name(self) -> str:
        return "Censys"

    def get_queries(self) -> dict:
        return {
            "Find OpenSSH services": 'services.software.name: "{software}"',
            "Find subdomains for domain": 'parsed.names: "{domain}"',
            "Find wildcard certs": 'parsed.names: "*.{domain}"',
            "Expired Let's Encrypt certs": 'parsed.issuer.common_name: "Let\'s Encrypt" AND NOT parsed.validity.end: [NOW TO *]',
            "Apache servers": 'services.software.cpe: "cpe:/a:apache:http_server"',
            "Specific CVE": 'services.vulnerabilities.cve: "{cve}"',
        }

    def render_query(self, template: str, params: dict) -> str:
        try:
            return template.format(**params)
        except KeyError as e:
            return f"[ERROR] Missing parameter: {e}"

