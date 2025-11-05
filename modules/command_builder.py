# recon_gui/utils/command_builder.py

def render_template(template: str, params: dict) -> str:
    """
    Renders a query template using the provided parameters.

    Example:
        template = 'services.software.name: "{software}"'
        params = {'software': 'OpenSSH'}
        → returns: services.software.name: "OpenSSH"
    """
    try:
        return template.format(**params)
    except KeyError as e:
        return f"[ERROR] Missing parameter: {e}"
