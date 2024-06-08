from manager import *

def main():
    manager = QueueManager()
    manager.read_file()
    manager.simulate()
    manager.show_stats()

if __name__ == "__main__":
    main()