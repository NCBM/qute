def topprint(*args, top: int = 1, **kwargs):
    print(f"\033[{top}A\n", *args, **kwargs)
    print(">>> ", end="", flush=True)