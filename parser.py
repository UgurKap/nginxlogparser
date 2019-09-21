import concurrent.futures, sys, time


# An example function to test multi-threads
# TODO: Remove this function
def do_something(sec):
    print(f"Sleeping {sec} second(s)")
    time.sleep(sec)
    return "Done sleeping..."


# This is where the multi-threading happens
with concurrent.futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(do_something, 1)
    f2 = executor.submit(do_something, 1)
    print(f1.result())
    print(f2.result())
