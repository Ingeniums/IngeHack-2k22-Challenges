import os
if __name__ == "__main__":
    for var in os.environ:
        del os.environ[var]
    os.environ["FLAG"] = "IngeHack{fake}"
    while True:
        _ = input('>>>') 
        eval(_) if len(_) <= 6 else print('try again')