# Nginx Log Parser
It parses nginx logs.

## How to Use?

From the commandline, user provides number of parser threads to be created and optionally name of the log file.
An additional thread is used for user interaction.

#### Example Usages:

python parser.py 4 ==> will read the logs using 4 threads.

python parser.py 100 access_old.log ==> will read the logs in "access_old.log" using 100 threads.