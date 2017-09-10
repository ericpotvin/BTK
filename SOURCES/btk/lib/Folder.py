""" Dir Module
"""
from os import path


class Folder(object):
    """ Dir Class
        Collect statistics regarding a folder
    """
    def __init__(self, name):
        """ Constructor
            :param name: The filename
        """
        self.name = name
        self.basename = path.basename(name)
        self.total_lines = 0
        self.covered_lines = 0
        self.files = []

    def add_file(self, file_object):
        """ Add statistics to the list
            :param file_object: The lib.File object
            :return: None
        """
        self.total_lines = self.total_lines + file_object.total_lines
        self.covered_lines = self.covered_lines + file_object.covered_lines
        self.files.append(file_object)
