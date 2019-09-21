import concurrent.futures, sys, os, mmap, contextlib


def read(file):
    """
    Reads lines of the given file until it hits an empty line.
    :param file: a file opened by mmap or os.open()
    :return: Nothing yet
    """

    line = file.readline()
    while line:
        print(line)
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


if __name__ == "__main__":
    main()
