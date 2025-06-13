# Parse open/openat lines and extract the filename in quotes using string methods

def extract_filename(line):
    # Look for 'open(' or 'openat('
    for prefix in ('open(', 'openat('):
        idx = line.find(prefix)
        if idx != -1:
            # Find the first quote after the prefix
            start = line.find('"', idx)
            if start != -1:
                end = line.find('"', start + 1)
                if end != -1:
                    return line[start + 1:end]
    return None

def is_wanted_file(filename):
    # Skip .pyc files
    if not (filename.endswith('.dat') 
        # or filename.endswith('.csh') 
        # or filename.endswith('.py') 
        # or filename.endswith('.pl') 
        # or filename.endswith('.log')
        # or filename.endswith('.csv')
        or filename.endswith('.dat')):
        # or filename.endswith('.txt')):
        return False

    # Skip common library directories
    unwanted_dirs = ('/lib', '/usr/lib', '/lib64', '/usr/share')
    for d in unwanted_dirs:
        if filename.startswith(d):
            return False
    return True

with open('strace.log', 'r') as f:
    for line in f:
        filename = extract_filename(line)
        if filename and is_wanted_file(filename):
            print(filename)