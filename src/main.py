from discovery import discover
from leaderElection import elections
def main():
    robots = discover.discover_neighbouring_devices()
    print(robots)
    leaderBot = elections.simulate_leader_election()
    print(leaderBot)

if __name__ == "__main__":
    main()
