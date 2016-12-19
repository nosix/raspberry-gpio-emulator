import fcntl
import os
import sys

from .Pipe import Pipe

client_rfd, server_wfd = os.pipe()
server_rfd, client_wfd = os.pipe()

pid = os.fork()

if pid == 0:
    # Child process
    from .UIClient import UI

    fcntl.fcntl(client_rfd, fcntl.F_SETFL, os.O_NONBLOCK)
    pipe = Pipe(os.fdopen(client_wfd, 'wb'), os.fdopen(client_rfd, 'rb'))
    ui = UI(pipe)
else:
    # Parent process
    from .UIServer import UI

    fcntl.fcntl(server_rfd, fcntl.F_SETFL, os.O_NONBLOCK)
    pipe = Pipe(os.fdopen(server_wfd, 'wb'), os.fdopen(server_rfd, 'rb'))
    try:
        ui = UI(pipe)
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
