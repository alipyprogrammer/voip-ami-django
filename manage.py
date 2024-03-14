#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading

import os
import threading
from django.core.management import execute_from_command_line

# تنظیم متغیرهای محیطی مورد نیاز برای Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

def start_print_task():
    os.system("python tasks.py")

if __name__ == "__main__":
    t = threading.Thread(target=start_print_task)
    t.daemon = True
    t.start()

    # اجرای خطوط فرمان مربوط به Django
    execute_from_command_line(sys.argv)




def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()
