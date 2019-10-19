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
    Given a line, it parses the line with regular expression patterns and saves them
    in corresponding variables as string objects.

    :param line: A line read by readline() function or a sequence of bytes in the same format as a line read by
                 readline(). It must be a sequence of bytes, otherwise regular expression patterns will fail.
    """

    remote_addresses.append(str(re.findall(b"[0-9]*.[0-9]*.[0-9]*.[0-9]*", line)[0]).lstrip("b'").rstrip("'"))
    remote_users.append(str(re.findall(b"-.*\[", line)[0]).lstrip("b'-").rstrip("[' "))
    request_times.append(str(re.findall(b"\[.*\]", line)[0]).lstrip("b'").rstrip("'"))
    requests.append(str(re.findall(b'".*" [0-9]', line)[0][0:-2]).lstrip("b'").rstrip("'"))

    # l is a placeholder variable, it holds response status and body_bytes sent respectively.
    l = str(re.findall(b'" [0-9]* [0-9]*', line)[0]).lstrip("b' \"").rstrip("'").split()
    statuses.append(l[0])
    bytes_sent.append(l[1])

    # l is a placeholder variable, it holds referrer, user_agent, gzip ratios respectively.
    l = str(re.findall(b'[0-9] ".*" ".*" ".*"', line)[0]).lstrip("b'").rstrip("'")[2:].split('" "')
    referrers.append(l[0].strip('"'))
    user_agents.append(l[1].strip('"'))
    gzip_ratios.append(l[2].strip('"'))


def read(file):

    """
    Reads lines of the given file and sends them to parse function until it hits an empty line.

    :param file: a file opened by mmap or os.open() (file must be opened in byte mode)
    """

    line = file.readline()
    while line:  # We are not even going to try to parse if line is empty.
        parse(line)
        line = file.readline()


def menu():

    """
    This function is the main program loop, it is intended to run in its own thread along with parser threads.
    """

    menu_text = """What do you want to see?
    h  : help
    q  : quit
    a  : remote_address
    u  : remote_user
    t  : time_local
    r  : requests
    s  : status
    b  : body_bytes_sent
    ref: http_referrer
    ag : user_agent
    g  : gzip_ratio"""

    print(menu_text)

    while True:
        print("Your choice:", end=" ")
        choice = input().lower()

        if choice == "q":
            break
        elif choice == "h":
            print(menu_text)

        choices = {"a": remote_addresses, "u": remote_users,
                   "t": request_times, "r": requests, "s": statuses,
                   "b": bytes_sent, "ref": referrers, "ag": user_agents,
                   "g": gzip_ratios}
        container = choices.get(choice)
        if container:
            print(*container, sep="\n")
        else:
            print("There is no such an option.")


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
                threads = [executor.submit(read, m) for _ in range(number_of_threads)]  # parser threads
                threads.append(executor.submit(menu))  # menu thread


if __name__ == "__main__":
    main()
