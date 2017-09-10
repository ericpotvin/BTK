""" Collect Module
"""
import os
import subprocess
from constants import DATA_BASE, PS4_DELIMITER, PS4_SEP
from File import File


class Collect(object):
    """ Collect Class
    """

    BASH_SCRIPT = ["bash", "-x"]

    def __init__(self):
        """ Constructor
        """
        self.files = {}
        self.sub_process = None
        self.pid = os.getpid()

    def process(self, args):
        """ Parse the output
            :param args: Command line arguments
            :return: None
        """
        self.sub_process = subprocess.Popen(
            self.BASH_SCRIPT + args,
            stderr=subprocess.PIPE
        )

        for lines in self.sub_process.communicate():
            if lines is None:
                continue

            for line in lines.decode("utf-8").split("\n"):
                self.handle_line(line.strip())

        self.save()

    def handle_line(self, line):
        """ Handle one line of stderr input
            :param line: The line
            :return: None
        """

        if line.find(PS4_DELIMITER + PS4_SEP) == -1:
            return

        _, file_name, line_number, _ = line.split(PS4_SEP)

        path = os.path.realpath(os.path.abspath(file_name))

        if path not in self.files:

            file_ = File(path)

            folder = os.path.dirname(DATA_BASE + file_.path)
            if not os.path.isdir(folder):
                os.makedirs(folder)

            self.files[path] = file_

        file_ = self.files[path]
        file_.add_line(line_number)
        file_.save(DATA_BASE + file_.path + ".collect.bin")

    def save(self):
        """ Save data
            :return: None
        """

        for file_ in self.files.values():
            file_.merge(DATA_BASE + file_.path + ".bin")
            if os.path.exists(DATA_BASE + file_.path + ".collect.bin"):
                os.unlink(DATA_BASE + file_.path + ".collect.bin")
