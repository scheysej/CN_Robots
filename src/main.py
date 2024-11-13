from discovery import discover

def main():
    robots = discover.discover_neighbouring_devices()
    print(robots)

if __name__ == "__main__":
    main()
