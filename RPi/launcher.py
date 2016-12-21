import os

from .pipe import Pipe

client_rfd, server_wfd = os.pipe()
server_rfd, client_wfd = os.pipe()

pid = os.fork()

if pid == 0:
    # Child process
    import signal
    import traceback
    import inspect
    from .ui_client import UI

    pipe = Pipe(os.fdopen(client_wfd, 'wb'), os.fdopen(client_rfd, 'rb'))
    ui = UI(pipe)


    def interrupt(signum, stack):
        s = stack
        while s.f_back is not None:
            s = s.f_back
        if inspect.getframeinfo(s).function != '_shutdown':
            traceback.print_stack(stack)


    signal.signal(signal.SIGINT, interrupt)
else:
    # Parent process
    import fcntl
    import sys
    from .ui_server import UI

    fcntl.fcntl(server_rfd, fcntl.F_SETFL, os.O_NONBLOCK)
    pipe = Pipe(os.fdopen(server_wfd, 'wb'), os.fdopen(server_rfd, 'rb'))
    ui = UI(pipe)
    try:
        ui.run()
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        ui.close()
