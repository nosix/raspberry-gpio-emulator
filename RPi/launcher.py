import fcntl
import os
import sys

from .pipe import Pipe

client_rfd, server_wfd = os.pipe()
server_rfd, client_wfd = os.pipe()

pid = os.fork()

if pid == 0:
    # Child process
    from .ui_client import UI

    fcntl.fcntl(client_rfd, fcntl.F_SETFL, os.O_NONBLOCK)
    pipe = Pipe(os.fdopen(client_wfd, 'wb'), os.fdopen(client_rfd, 'rb'))
    ui = UI(pipe)
else:
    # Parent process
    from .ui_server import UI

    fcntl.fcntl(server_rfd, fcntl.F_SETFL, os.O_NONBLOCK)
    pipe = Pipe(os.fdopen(server_wfd, 'wb'), os.fdopen(server_rfd, 'rb'))
    try:
        ui = UI(pipe)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
