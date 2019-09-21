import concurrent.futures
import contextlib
import mmap
import sys
import re

remote_addresses = []
remote_users = []
request_times = []
requests = []
statuses = []
bytes_sent = []
referrers = []
user_agents = []
gzip_ratios = []


def parse(line):
    """
    Given a line, it parses the line and saves them in corresponding variables as string objects.
    :param line: A line read by readline() function or a sequence of bytes in the same format as a line read by
                 readline(). It must be a sequence of bytes, otherwise regular expression patterns will fail.
    :return: -
    """
    remote_addresses.append(str(re.findall(b"[0-9]*.[0-9]*.[0-9]*.[0-9]*", line)[0]).lstrip("b'").rstrip("'"))
    remote_users.append(str(re.findall(b"-.*\[", line)[0]).lstrip("b'-").rstrip("[' "))
    request_times.append(str(re.findall(b"\[.*\]", line)[0]).lstrip("b'").rstrip("'"))
    requests.append(str(re.findall(b'".*" [0-9]', line)[0][0:-2]).lstrip("b'").rstrip("'"))

    # l is a placeholder variable, it holds response status and body_bytes sent respectively.
    l = str(re.findall(b'" [0-9]* [0-9]*', line)[0]).lstrip("b' \"").rstrip("'").split()
    statuses.append(l[0])
    bytes_sent.append(l[1])

    # l is a placeholder variable, it holds referrer, user_agent, gzip ratios respectively
    l = str(re.findall(b'[0-9] ".*" ".*" ".*"', line)[0]).lstrip("b'").rstrip("'")[2:].split()
    referrers.append(l[0].strip('"'))
    user_agents.append(l[1].strip('"'))
    gzip_ratios.append(l[2].strip('"'))





def read(file):
    """
    Reads lines of the given file until it hits an empty line.
    :param file: a file opened by mmap or os.open()
    :return: Nothing yet
    """

    line = file.readline()
    while line:  # We are not even going to try to parse if line is empty.
        parse(line)
        line = file.readline()


def main():
    # Number of threads will be given by the user as a commandline argument
    number_of_threads = int(sys.argv[1])

    # We may be given another name then access.log as a commandline as well
    try:
        log_name = sys.argv[2]
    except IndexError:
        log_name = "access.log"  # Default name if one is not provided

    # We will open the file using a memory map, our performance will be increased since
    # we are accessing the memory directly.
    with open(log_name, "r") as f:
        with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as m:
            # This part is where we are using multi-threading
            with concurrent.futures.ThreadPoolExecutor() as executor:
                threads = [executor.submit(read, m) for _ in range(number_of_threads)]

                # for thread in concurrent.futures.as_completed(threads):
                #     thread.result()

    # for a in remote_addresses:
    #     print(a)
    #
    # for u in remote_users:
    #     print(u)
    #
    # for t in request_times:
    #     print(t)
    #
    # for r in requests:
    #     print(r)


if __name__ == "__main__":
    main()
