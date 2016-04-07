import datetime
import os


class CSVLog:
    """
    Creates a log object that can append data to a cvs file.  When a new log is written to file, it is located in
    'log/{name}-{creation time}.csv'.
    """
    def __init__(self, name, *titles):
        """
        Creates a new CSVLog, which will save to a given name.

        :param name: The name which will be used when the log is saved.
        :param titles: An optional list of strings to use as titles for the columns in the log.
        :return: The new CSVLog.
        """
        self.name = name
        self.content = ",".join(titles)

    def append(self, *args):
        """
        Appends new data to the log.

        :param args: The data to append to the log.  Will ultimately manifest as a line a csv file.
        """
        # Turn all arguments into strings
        data = []
        for arg in args:
            data.append(str(arg))

        # Add a new line if content already exists in the file.
        self.content += '\n' if self.content != '' else ''

        # Add the new data.
        self.content += ",".join(data)

    def write(self):
        """
        Writes the current log to a csv file.  The file will be saved in 'log/{name}-{creation time}.csv'.
        """
        # Make sure the directory for output exists
        if not os.path.exists('log'):
            os.makedirs('log')

        f = open('log/%s-%s.csv' % (self.name, datetime.datetime.now().strftime('%m-%d-%y-%H-%M')), 'w+')

        f.write(self.content)