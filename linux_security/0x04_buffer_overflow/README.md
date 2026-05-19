# Buffer Overflow

## 0. Hack the VM

This project demonstrates how to locate the heap segment of a running Linux process and replace a string inside that process memory without stopping it.

The script `read_write_heap.py` reads `/proc/<pid>/maps`, finds the `[heap]` memory range, opens `/proc/<pid>/mem`, searches only inside the heap, and replaces the target ASCII string.

## Usage

    sudo python3 ./read_write_heap.py pid search_string replace_string

Example:

    sudo python3 ./read_write_heap.py 6515 Holberton maroua
