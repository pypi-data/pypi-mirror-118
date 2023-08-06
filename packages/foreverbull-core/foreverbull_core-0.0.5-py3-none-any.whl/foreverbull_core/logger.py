import logging
import logging.config
import pathlib


class Logger:
    def __init__(self):
        self.current_folder = pathlib.Path(__file__).parent.resolve()
        self.config_file = self.current_folder / 'logger.conf'
        logging.config.fileConfig(str(self.config_file.absolute()))

    def configure(self, mode = "base"):
        logging.getLogger(mode)
