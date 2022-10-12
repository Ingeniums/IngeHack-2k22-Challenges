import os
if __name__ == "__main__":
    for var in os.environ:
        del os.environ[var]
    os.environ["FLAG"] = "IngeHack{help()_r34ally_h3lp_;)}"
    while True:
        _ = input('>>>') 
        eval(_) if len(_) <= 6 else print('try again')