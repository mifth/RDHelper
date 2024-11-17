import renderdoc as rd
import qrenderdoc as qrd

from . import rdh_main

extiface_version = ''
cur_window: rdh_main.RDHWindow = None


def retrieve_window(ctx, version):
    global cur_window

    if cur_window:
        cur_window.ctx.RemoveCaptureViewer(cur_window)
        del cur_window
        cur_window = rdh_main.RDHWindow(ctx, version)
    else:
        cur_window = rdh_main.RDHWindow(ctx, version)

    return cur_window.main_widget


def open_window_callback(ctx: qrd.CaptureContext, data):
    widged_window = retrieve_window(ctx, extiface_version)

    ctx.RaiseDockWindow(widged_window)


def register(version: str, ctx: qrd.CaptureContext):
    global extiface_version
    extiface_version = version

    print("Registering RDHelper for RenderDoc version {}".format(version))

    ctx.Extensions().RegisterWindowMenu(qrd.WindowMenu.Window, ["RDHelper Window"], open_window_callback)
    print("RDHelper is added!")


def unregister():
    global cur_window
    cur_window.ctx.RemoveCaptureViewer(cur_window)
    
    if cur_window:
        del cur_window
        cur_window = None
    print("RDHelper is removed!")



