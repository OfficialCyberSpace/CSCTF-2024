import io
from pickle import *
from functools import partial
import sandbox


class RestrictedUnpickler(Unpickler):
    def find_class(self, mod: str, attr: str):
        if attr == "SandboxClass":
            return sandbox.SandboxClass
        if attr == "sandbox":
            return sandbox

        # true wizardry
        if attr == "partial":
            return partial
        if attr == "next":
            return next
        if attr == "iter":
            return iter


class LessRestrictedUnpickler(Unpickler):
    def find_class(self, mod: str, attr: str):
        assert mod == "sandbox"
        return Unpickler.find_class(self, mod, attr)


p = bytes.fromhex(input("> "))
assert len(p) < 318

LessRestrictedUnpickler(io.BytesIO(dumps(*RestrictedUnpickler(io.BytesIO(p)).load()))).load()
