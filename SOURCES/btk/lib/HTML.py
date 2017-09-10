""" HTML Module
"""
import time
from os.path import exists

from constants import SHARE_PATH
from File import File
from Severity import Severity
from Statistics import Statistics


class HTML(object):
    """ HTML Class
        Get the content of HTML for the report
    """
    INDEX_FILE = "index"
    FILE_EXT = ".html"
    LINK_ROOT = "root"

    HEADER = "header"
    GO_BACK_LINK = "go_back_link"
    TABLE_HEADER = "table_header"
    TABLE_LINE = "table_line"
    FOOTER_TOTAL = "footer_total"
    FOOTER = "footer"
    SRC_PREFIX = "src_prefix"
    SRC_SUFFIX = "src_suffix"
    SRC_LINE_PREFIX = "src_line_prefix"
    LINE_SOURCE = "line_source"

    def __init__(self):
        """ Constructor
        """
        pass

    @staticmethod
    def get_html(filename):
        """ Get the HTML for a file
            :param filename: The HTML filename
            :return: string
        """
        html_file = SHARE_PATH + filename + HTML.FILE_EXT

        if not exists(html_file):
            return ""
        return File.read_file(html_file).decode('utf-8')

    @staticmethod
    def get_header(basename, html_tag):
        """ Write the header of the file
            :param basename: The base name
            :param html_tag: The html tag/constant
            :return: None
        """
        header = HTML.get_html(HTML.HEADER) % (
            SHARE_PATH,
            basename,
            time.strftime("%Y-%m-%d %H:%M:%S")
        )

        return header + HTML.get_html(html_tag)

    @staticmethod
    def get_footer(total_lines, covered_lines, show_total=True):
        """ Write the footer of a file
            :param total_lines: The number of files
            :param covered_lines: The number of lines covered
            :param show_total: Hide the totals and legend
            :return: None
        """
        footer = ""

        if show_total:
            total_lines = 1 if total_lines == 0 else total_lines
            ratio = Statistics.get_ratio(covered_lines, total_lines)
            footer = HTML.get_html(HTML.FOOTER_TOTAL) % (
                Severity.get_color(ratio),
                ratio,
                total_lines,
                covered_lines
            )

        return footer + HTML.get_html(HTML.FOOTER)

    @staticmethod
    def get_line(link_name, name, total_lines, covered_lines):
        """ Write headers
            :param link_name: The anchor name
            :param name: the name
            :param total_lines: Total lines processed
            :param covered_lines: Total lines covered
            :return: string
        """

        ratio = Statistics.get_ratio(covered_lines, total_lines)
        color = Severity.get_color(ratio)

        return HTML.get_html(HTML.TABLE_LINE) % (
            color,
            link_name,
            name,
            color,
            ratio,
            ratio,
            covered_lines,
            total_lines
        )

    @staticmethod
    def get_link(path, link_root, link):
        """ Get the anchor link
            :param path: The path
            :param link_root: The link/href
            :param link: The link name
            :return: string
        """
        return HTML.get_html(HTML.GO_BACK_LINK) % (path, link_root, link)
