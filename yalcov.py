#!/usr/bin/env python

import sqlite3

conn = sqlite3.connect('yalcov')

class yalcov:
    def __init__(self, logfile):
        self.logfn = logfile
        logf = open(self.logfn, "r")
        parse_log(logf)
        report()

    def parse_log(self, logf):
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE cov
                       (filepath text, line real, hitcnt real)''')

        for line in logf.readlines():
            lineno = line.split(':')[1]
            path = line.split(':')[0]

            c.execute("SELECT hitcnt FROM cov WHERE filepath = '%s' AND line = '%d'" % path, lineno)
            row = cur.fetchone()
            if row is None:
                # Insert a row of data
                c.execute("INSERT INTO cov VALUES (%s, %d, 1)" % path, lineno)
            else:
                c.execute("UPDATE cov SET hitcnt = hitcnt + 1 WHERE filepath = '%s' AND line = '%d'" % path, lineno)

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
                print '%4d|%4d|%s' % lineno, hitcnt, line

            srcfile.close()

def main(argv):
    yc = yalcov(argv[0])

if __name__ == '__main__':
    main(sys.argv[1:])
