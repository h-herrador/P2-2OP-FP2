from manager import *

def main():
    manager = QueueManager()
    manager.read_file()
    manager.simulate()

if __name__ == "__main__":
    main()