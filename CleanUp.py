import re
from Util import get_file_paths


### Just a simple script to remove MD formatting, should be moved to util class

paths = get_file_paths('.')

for path in paths:
    with open(path, 'r+', encoding='utf-8') as f:
        file_content = f.read()
        updated_content = re.sub(r'[-|]+', ' ', file_content)
        f.seek(0)
        f.truncate()
        f.write(updated_content)


