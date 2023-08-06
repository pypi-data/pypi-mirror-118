import os
import json
import platform
from ctypes import cdll


if platform.uname()[0] == "Windows":
    _lib_filename = "cls_ffi.dll"
elif platform.uname()[0] == "Linux":
    _lib_filename = "libcls_ffi.so"
elif platform.uname()[0] == "Darwin" and platform.uname().machine == "arm64":
    _lib_filename = "libcls_ffi_arm64.dylib"
elif platform.uname()[0] == "Darwin":
    _lib_filename = "libcls_ffi.dylib"
else:
    raise Exception("Unknown platform for CLS")


_lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), "libs", _lib_filename))


def set_debug(debug):
    _lib.set_debug(1 if debug else 0)


def set_project_key(project_key):
    _lib.set_project_key(project_key.encode("utf-8"))


def set_project_slug(project_slug):
    _lib.set_project_slug(project_slug.encode("utf-8"))


def set_noninteractive_tracking_enabled(enabled):
    _lib.set_noninteractive_tracking_enabled(1 if enabled else 0)


def track_event(slug, type, metadata, dispatch):
    _lib.track_event(
        slug.encode("utf-8"),
        type.encode("utf-8"),
        json.dumps(metadata).encode("utf-8"),
        1 if dispatch else 0,
    )


def dispatch_events():
    _lib.dispatch_events()


def set_request_permission_prompt(prompt):
    _lib.set_request_permission_prompt(prompt.encode("utf-8"))


def set_user_id(user_id):
    _lib.set_user_id(user_id.encode("utf-8"))


def set_invocation_id(invocation_id):
    _lib.set_invocation_id(invocation_id.encode("utf-8"))


def set_is_noninteractive(is_noninteractive):
    _lib.set_is_noninteractive(1 if is_noninteractive else 0)
