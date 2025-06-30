import os
# import sys
# import tty
import msvcrt  # Windows
# import termios  # Unix etc.

# Windows
if os.name == 'nt':
    def input_password(prompt='Password: '):
        print(prompt, end='', flush=True)
        password = ''
        while True:
            char = msvcrt.getch()
            if char in {b'\r', b'\n'}:
                print()
                break
            elif char == b'\x08':  # Backspace dinges
                if password:
                    password = password[:-1]
                    print('\b \b', end='', flush=True)
            elif char == b'\x03':  # Ctrl+C action
                raise KeyboardInterrupt
            else:
                try:
                    decoded_char = char.decode('utf-8')
                except UnicodeDecodeError:
                    continue
                password += decoded_char
                print('*', end='', flush=True)
        return password

# Unix based systems, zoals MacOS of Linux
# else:
#     def input_password(prompt='Password: '):
#         print(prompt, end='', flush=True)
#         password = ''
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(fd)
#             while True:
#                 char = sys.stdin.read(1)
#                 if char in {'\r', '\n'}:
#                     print()
#                     break
#                 elif char == '\x7f':  # Backspace dinges
#                     if len(password) > 0:
#                         password = password[:-1]
#                         print('\b \b', end='', flush=True)
#                 elif char == '\x03':  # Ctrl+C action
#                     raise KeyboardInterrupt
#                 else:
#                     password += char
#                     print('*', end='', flush=True)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return password
