#!/usr/bin/python3
"""Find and replace a string inside the heap of a running process."""

import sys


def usage():
    print("Usage: read_write_heap.py pid search_string replace_string")
    sys.exit(1)


def get_heap(pid):
    """Return heap start and end addresses."""
    try:
        with open(f"/proc/{pid}/maps", "r", encoding="utf-8") as maps:
            for line in maps:
                if "[heap]" in line:
                    addresses = line.split()[0]
                    start, end = addresses.split("-")
                    return int(start, 16), int(end, 16)
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)

    print("Error: heap not found")
    sys.exit(1)


def main():
    """Main function."""
    if len(sys.argv) != 4:
        usage()

    pid = sys.argv[1]
    search_string = sys.argv[2].encode("ascii")
    replace_string = sys.argv[3].encode("ascii")

    if len(replace_string) > len(search_string):
        print("Error: replace_string must be shorter than or equal to search_string")
        sys.exit(1)

    replace_string = replace_string.ljust(len(search_string), b"\x00")

    heap_start, heap_end = get_heap(pid)

    try:
        with open(f"/proc/{pid}/mem", "r+b", 0) as mem:
            mem.seek(heap_start)
            heap = mem.read(heap_end - heap_start)

            index = heap.find(search_string)
            if index == -1:
                print("Error: string not found in heap")
                sys.exit(1)

            address = heap_start + index
            mem.seek(address)
            mem.write(replace_string)

            print(f"Heap: {hex(heap_start)}-{hex(heap_end)}")
            print(f"Found at: {hex(address)}")
            print("String replaced")
    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
