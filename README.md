# Joystick-Controlled Convoy Protocol for Secure Communication and Coordination

This project focuses on developing a convoy protocol that enables road hazard detection and secure communication between autonomous vehicles using a joystick-controlled system. The protocol supports functions such as leader election, secure command transmission, and dynamic joining of new vehicles.

## Project Overview

This system aims to:
1. Discover and initialize robots and joystick controllers.
2. Elect a leader among robots for centralized command management.
3. Enable secure communication between joystick and the leader.
4. Broadcast commands securely from the leader to other robots.
5. Allow dynamic joining of new robots into the convoy.
6. Ensure security through encryption and authentication mechanisms.

```
CN_Robots
├── README.md
├── src/
│   ├── main.py
│   ├── request_join.py
│   ├── discovery/
│   ├── leader_election/
│   ├── joystick_communication/
│   ├── command_broadcast/
│   ├── dynamic_joining/
│   ├── utils/
│   └── security_authentication/
└── tests/
```

## Milestone \#1 (Due: November 29<sup>th</sup>, 2024)
- **Objective**: Complete setup of scripts, libraries, dependencies, and basic robot communication.
- **Tasks**:
  - **Discovery Protocol**: Establish UDP-based discovery for robots and joysticks.
  - **Leader Election**: Implement a consensus protocol for leader selection.
  - **Joystick Communication**: Set up unicast communication between the joystick and the elected leader.
  - **Command Broadcasting**: Enable encrypted command broadcasting from the leader to other robots.
  - **Dynamic Joining**: Develop a protocol to allow new robots to join the convoy dynamically.
  - **Security and Authentication**: Implement encryption and authentication for secure convoy communications.

## Milestone \#2 (Due: December 6<sup>th</sup>, 2024)
- **Objective**: Complete all remaining tasks, including final testing and project demonstration.

## Folder Structure

- **src/**: All source code organized by task area.
- **tests/**: Contains testing scripts for each functionality.

---
