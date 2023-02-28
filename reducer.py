#!/usr/bin/env python3

import sys

current_date = None
current_type = None
current_count = 0

for line in sys.stdin:
    date, obj_type, count = line.strip().split('\t')
    count = int(count)

    if date == current_date and obj_type == current_type:
        current_count += count
    else:
        if current_date and current_type:
            print(f'{current_date}\t{current_type}\t{current_count}')
        current_date = date
        current_type = obj_type
        current_count = count

if current_date and current_type:
    print(f'{current_date}\t{current_type}\t{current_count}')