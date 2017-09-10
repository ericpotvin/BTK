""" File Module
"""
import pickle
import stat
from hashlib import md5
from os import path, lstat


class File(object):
    """ File Class
    """
    def __init__(self, folder, source_folder=None):
        """ Constructor
            :param folder: The path
            :param source_folder: The source path
        """
        self.path = folder
        self.source_path = folder if source_folder is None else source_folder
        self.basename = path.basename(folder)
        self.lines = {}

        key = md5()
        key.update(File.read_file(self.source_path))

        file_stats = lstat(self.source_path)
        self.source_file_ctime = file_stats[stat.ST_CTIME]

        self.digest = key.digest()

    def get_source_ctime(self):
        """ Return the creation time of the script
            :return: string
        """
        return self.source_file_ctime

    def set_source_path(self, folder):
        """ Set the source path
            :param folder: The path
            :return: None
        """
        self.source_path = folder

    def get_source_path(self):
        """ Get the source path
            :return: string
        """
        return self.source_path

    def save(self, filename):
        """ Save the file
            :param filename: The filename
            :return: None
        """
        outfile = open(filename, 'wb')
        pickle.dump(self, outfile)
        outfile.close()

    def merge_object(self, obj):
        """ Merge another object into this
            :param obj: The object to merge
            :return: None
        """
        for key, value in obj.lines.items():
            if key not in self.lines:
                self.lines[key] = value
            self.lines[key] = self.lines[key] + value

    @staticmethod
    def load(filename, script_base_path=""):
        """ Load a file
            :param filename: The filename
            :param script_base_path: The script base path
            :return: pickle object
        """
        file_ = pickle.load(open(filename, 'rb'))
        source_file = File.read_file(script_base_path + file_.path)

        key = md5()
        key.update(source_file)
        digest = key.digest()

        if digest != file_.digest:
            file_ = File(file_.path, script_base_path + file_.path)
            file_.set_source_path(script_base_path + file_.path)

        return file_

    @staticmethod
    def read_file(name):
        """ Read content of a file
            :param name: The filename
        """
        with open(name, 'r') as my_file:
            return my_file.read().encode('utf-8')

    def merge(self, filename):
        """ Merge files
            :param filename: The filename to merge
            :return: None
        """

        if path.exists(filename):
            file_fd = open(filename, 'rb')
            src = pickle.load(file_fd)
            file_fd.seek(0)
            if src.digest == self.digest:
                self.merge_object(src)
            file_fd.close()

        file_fd = open(filename, 'wb')
        pickle.dump(self, file_fd)
        file_fd.close()

    def add_line(self, line_number):
        """ Add lines
            :param line_number: The line number
            :return: None
        """
        line_number = int(line_number)

        if line_number not in self.lines:
            self.lines[line_number] = 0

        self.lines[line_number] += 1
