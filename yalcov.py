#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import sqlite3
from optparse import OptionParser


try:
    os.remove('yalcov.db')
except OSError:
    pass

conn = sqlite3.connect('yalcov.db')


class yalcov:
    mask_cnt = False

    def __init__(self, logfile, mc):
        self.logfn = logfile
        self.mask_cnt = mc
        logf = open(self.logfn, "r")
        self.parse_log(logf)
        self.report()

    def parse_log(self, logf):
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE cov
                       (filepath text, line int, hitcnt int)''')

        for line in logf.readlines():
            lineno = int(line.split(':')[1])
            path = line.split(':')[0]

            c.execute("SELECT hitcnt FROM cov WHERE filepath = '%s' AND line = '%d'" % (path, lineno))
            row = c.fetchone()
            if row is None:
                # Insert a row of data
                c.execute("INSERT INTO cov VALUES (?, ?, 1)", (path, lineno))
            else:
                c.execute("UPDATE cov SET hitcnt = hitcnt + 1 WHERE filepath = '%s' AND line = '%d'" % (path, lineno))

            # Save (commit) the changes
            conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        # conn.close()

    def report(self):
        c = conn.cursor()

        c.execute('''SELECT filepath FROM cov''')
        rows = c.fetchall()
        files = []
        for row in rows:
            files.append(row[0])

        for f in files:
            c.execute("SELECT * FROM cov WHERE filepath = '%s' ORDER BY line" % f)
            filecov = c.fetchall()

            linecov = {}
            for row in filecov:
                linecov[row[1]] = row[2]

            lineno = 1
            srcfile = open(f, "r")
            for line in srcfile:
                hitcnt = 0
                if lineno in linecov:
                    hitcnt = linecov[lineno]
                    if self.mask_cnt:
                        hitcnt = 1
                print('%4d|%4d|%s' % (lineno, hitcnt, line), end='')
                lineno = lineno + 1

            srcfile.close()


def main(argv):
    parser = OptionParser()
    parser.add_option("-m", "--mask-cnt", action="store_true", dest="mask_cnt", default=False,
                                        help="ignore hit count in report, set hit count to 1 for any value >= 1")
    (options, args) = parser.parse_args(argv)
    yalcov(args[0], options.mask_cnt)

if __name__ == '__main__':
    main(sys.argv[1:])
