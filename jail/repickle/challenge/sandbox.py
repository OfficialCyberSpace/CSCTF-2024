class SandboxClass:
    def __reduce__(self):
        return SandboxClass, ()
