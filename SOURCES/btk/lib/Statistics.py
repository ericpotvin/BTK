""" Statistics Module
"""
from Code import Code
from File import File


class Statistics(object):
    """ Statistics class
    """

    @staticmethod
    def calculate(file_):
        """ Calculate the statistics
            :param file_: The file object
            :return: None
        """
        file_.total_lines = 0
        file_.covered_lines = 0
        processed_line = 1
        count_covered = False
        lines = File.read_file(file_.get_source_path()).splitlines()

        for line in lines:
            line = line.decode("utf-8")
            if Code.line_is_code(line):
                file_.total_lines = file_.total_lines + 1
                if processed_line in file_.lines or count_covered:
                    file_.covered_lines = file_.covered_lines + 1

            count_covered = True if line.endswith("\\") else False

            processed_line += 1

    @staticmethod
    def get_ratio(numerator, denominator):
        """
            :param numerator:
            :param denominator:
            :return:
        """
        return (float(numerator) / float(denominator)) * 100
