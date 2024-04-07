import pickle

def write_pair(path, start, end) -> None:
    with open(path, "w") as file:
        file.write(f"{start}\n{end}")

def read_pair(path) -> tuple[int, int]:
    with open(path, "r") as file:
        start, end = file.read().splitlines()
        file.close()
    return (int(start), int(end))

def save_data(blocks, path) -> None:
    with open(path, "wb") as file:
        pickle.dump(blocks, file)
        file.close()
    return

def load_data(path) -> list:
    with open(path, "rb") as file:
        blocks = pickle.load(file)
        file.close()
    return blocks

def write_string(data, path):
    with open(path, "w") as file:
        file.write(data)
        file.close()

def read_string(path):
    with open(path, "r") as file:
        data = file.read()
        file.close()
    return data
