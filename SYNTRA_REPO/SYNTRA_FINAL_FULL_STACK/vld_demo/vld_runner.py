# Simple VLD Runner (Demo)
print("[VLD] Running symbolic logic from test.vld...")
with open("test.vld") as f:
    for line in f:
        print("Executing:", line.strip())
