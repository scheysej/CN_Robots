from discovery import discover

def main():
    robots = discover.discover_neighbouring_robots()
    print(robots)

if __name__ == "__main__":
    main()
