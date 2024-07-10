import argparse

if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="One-way folder synchronization")
    parser.add_argument("-s", "--source", type=str,
                        default="source", help="Source folder path")
    parser.add_argument("-r", "--replica", type=str,
                        default="replica", help="Replica folder path")
    parser.add_argument("-i", "--interval", type=int, default=60,
                        help="Synchronization interval (in seconds)")
    parser.add_argument("-l", "--log-file", type=str,
                        default="log.txt", help="Log file path")

    args = parser.parse_args()
