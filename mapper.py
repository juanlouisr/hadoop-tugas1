#!/usr/bin/env python3
"""mapper.py"""

import sys
import json
from datetime import datetime

def extract_type(obj):
    """Helper function to extract the 'type' field from a JSON object."""
    if 'object' in obj and 'social_media' in obj['object']:
        return obj['object']['social_media']
    elif 'crawler_target' in obj and 'specific_resource_type' in obj['crawler_target']:
        return obj['crawler_target']['specific_resource_type']
    else:
        return None

for line in sys.stdin:
    try:
        data = json.loads(line)
        for obj in data:
            created_time = obj.get('created_time')
            if created_time:
                if created_time.isdigit():
                    # epoch
                    created_time = datetime.fromtimestamp(int(created_time))
                else:
                    # 2021-01-26T03:20:27+0000
                    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S%z')

            if not created_time:
                created_time = obj.get('created_at')
                if created_time:
                    # Tue Jun 01 10:13:06 +0000 2021
                    created_time = datetime.strptime(created_time, '%a %b %d %H:%M:%S %z %Y')

            if not created_time:
                created_time = obj['snippet'].get('publishedAt')
                if created_time: 
                    # 2021-04-20T12:52:55Z
                    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%SZ')

            if not created_time:
                created_time = obj['snippet'].get('topLevelComment').get('snippet').get('publishedAt')
                if created_time: 
                    # 2021-04-20T12:52:55Z
                    created_time = datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%SZ')

            obj_type = extract_type(obj)
            if created_time and obj_type:
                # Convert epoch timestamps to formatted datetime strings
                print(f'{created_time.date()}\t{obj_type}\t1')
    except:
        continue