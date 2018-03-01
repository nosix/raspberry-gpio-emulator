import os

from .pipe import Pipe

client_rfd, server_wfd = os.pipe()
server_rfd, client_wfd = os.pipe()

pid = os.fork()

if pid != 0:
    # Parent process (UI client)
    import signal
    from .ui_client import UI

    pipe = Pipe(os.fdopen(client_wfd, 'wb'), os.fdopen(client_rfd, 'rb'))
    ui = UI(pipe)


    def interrupt(signum, stack):
        ui.interrupt_main_to_close = False
        import sys
        import traceback
        traceback.print_stack(stack)
        sys.exit(1)


    signal.signal(signal.SIGINT, interrupt)
else:
    # Child process (UI server)
    import argparse
    import fcntl
    import importlib
    import sys
    from .ui_server import UI

    parser = argparse.ArgumentParser(description='RPi.GPIO emulator.')
    parser.add_argument('plugin_module', type=str, nargs='*',
                        help='Plugin modules that have create_plugin() function')
    parser.add_argument('--ui', dest='ui_module', default='.ui_frame', help='GUI module that has create_ui() function')
    args = parser.parse_args()

    ui_module = importlib.import_module(args.ui_module, 'RPi')

    plugin_modules = map(importlib.import_module, args.plugin_module)
    plugins = list(map(lambda m: m.create_plugin(), plugin_modules))
    fcntl.fcntl(server_rfd, fcntl.F_SETFL, os.O_NONBLOCK)
    pipe = Pipe(os.fdopen(server_wfd, 'wb'), os.fdopen(server_rfd, 'rb'))

    ui = UI(pipe, ui_module.create_ui(), plugins)
    try:
        ui.run()
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        ui.close()
