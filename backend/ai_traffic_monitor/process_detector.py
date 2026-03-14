import psutil

IDE_PROCESSES = [
    "Code.exe",      # VS Code
    "cursor.exe",    # Cursor IDE
]

def detect_ide_usage():

    for process in psutil.process_iter(['name']):

        try:

            if process.info['name'] in IDE_PROCESSES:

                return process.info['name']

        except:
            continue

    return None