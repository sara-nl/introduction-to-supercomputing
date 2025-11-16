import sys
import time
import ctypes
# ##################################
# sleep for n seconds and print
# - cpu number
# - start time
# - end time


def get_cpu():
    """
    get the CPU id of the current process
    """
    libc = ctypes.CDLL(None)
    libc.sched_getcpu.restype = ctypes.c_int
    n = libc.sched_getcpu()
    if n >= 0:
        return n


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <seconds>", file=sys.stderr)
        sys.exit(1)
    try:
        n = float(sys.argv[1])
        if n < 0:
            raise ValueError("seconds must be non-negative")
    except ValueError as e:
        print(f"Invalid seconds value: {e}", file=sys.stderr)
        sys.exit(1)

    cpu = get_cpu()
    start = time.time()
    time.sleep(n)
    end = time.time()
    print(f"TASK {cpu} {start:.6f} {end:.6f}")


if __name__ == "__main__":
    main()
