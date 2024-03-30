import pickle

def write_endpoints(path, start, end) -> None:
    with open(path, "w") as file:
        file.write(f"{start}\n{end}")

def read_endpoints(path) -> tuple[int, int]:
    with open(path, "r") as file:
        start, end = file.read().splitlines()
        file.close()
    return (int(start), int(end))

def save_blocks(blocks, path) -> None:
    with open(path, "wb") as file:
        pickle.dump(blocks, file)
        file.close()
    return

def load_blocks(path) -> list:
    with open(path, "rb") as file:
        blocks = pickle.load(file)
        file.close()
    return blocks

