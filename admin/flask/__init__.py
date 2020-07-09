
from flask import Flask

class CustomFlask(Flask):
    """Custom version of Flask with our bells and whistles."""

    def __init__(self, import_name, config_file=None, debug=None,
                 use_flask_uuid=False,
                 *args, **kwargs):
        """Create an instance of Flask app.
        See original documentation for Flask.
        Args:
            import_name (str): Name of the application package.
            config_file (str): Path to a config file that needs to be loaded.
                Should be in a form of Python module.
            debug (bool): Override debug value.
            use_flask_uuid (bool): Turn on Flask-UUID extension if set to True.
        """
        super(CustomFlask, self).__init__(import_name, *args, **kwargs)
        if config_file:
            self.config.from_pyfile(config_file)
        if debug is not None:
            self.debug = debug
