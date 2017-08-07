# yalcov
Yet another line coverage tool.

Reading the log files containing file path and lineno, and generate the line coverage report.

##Input:


    /home/hailin/Documents/Dev/coreutils-6.10/src/tac.c:576
    /home/hailin/Documents/Dev/coreutils-6.10/src/tac.c:576
    /home/hailin/Documents/Dev/coreutils-6.10/src/tac.c:577

##Output:


       1|   0|/* tac - concatenate and print files in reverse
       2|   0|   Copyright (C) 1988-1991, 1995-2006 Free Software Foundation, Inc.
       ...
     576|   2|   bool ok;
     577|   1|   size_t half_buffer_size;


