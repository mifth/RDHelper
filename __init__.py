import renderdoc as rd
import qrenderdoc as qrd

from . import rdh_main

extiface_version = ''


def retrieve_window(ctx, version):
    if rdh_main.the_window:
        rdh_main.the_window.ctx.RemoveCaptureViewer(rdh_main.the_window)
        del rdh_main.the_window
        rdh_main.the_window = rdh_main.RDHCaptureViewer(ctx, version)
    else:
        rdh_main.the_window = rdh_main.RDHCaptureViewer(ctx, version)

    return rdh_main.the_window.main_widget


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
    rdh_main.the_window.ctx.RemoveCaptureViewer(rdh_main.the_window)
    
    if rdh_main.the_window:
        del rdh_main.the_window
        rdh_main.the_window = None
    print("RDHelper is removed!")



