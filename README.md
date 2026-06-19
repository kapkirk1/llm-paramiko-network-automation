# LLM Paramiko Network Automation

A Python-based network automation tool that uses a local LLM through Ollama to convert natural language requests into network CLI commands and execute them on Cisco devices via SSH using Paramiko.

## Features

* Natural language interface for network operations
* Local LLM inference using Ollama
* Multi-device command execution
* Multi-command execution per device
* SSH connectivity using Paramiko
* JSON-based communication between the LLM and automation engine
* Device inventory validation
* Error handling for:

  * Invalid JSON responses
  * Unknown devices
  * SSH connection failures

## Technologies Used

* Python
* Ollama
* Llama 3.2 1B
* Paramiko
* JSON
* Cisco IOS
* GNS3

## Project Workflow

User Request

↓

Ollama LLM

↓

Structured JSON Response

↓

Device Validation

↓

SSH Connection

↓

Command Execution

↓

Output Display

## Example Request

```text
Show interface status and routing table on r1 and r2
```

LLM Response:

```json
{
  "devices": ["r1", "r2"],
  "commands": [
    "show ip interface brief",
    "show ip route"
  ]
}
```

The application then:

1. Connects to r1
2. Executes all requested commands
3. Disconnects
4. Connects to r2
5. Executes all requested commands
6. Disconnects

## Inventory Example

```python
inventory = {
    'r1': {
        'hostname': '192.168.56.116',
        'username': 'cisco',
        'password': 'cisco',
        'look_for_keys': False
    },
    'r2': {
        'hostname': '192.168.56.115',
        'username': 'admin',
        'password': 'admin',
        'look_for_keys': False
    }
}
```

Update the inventory values to match your own lab environment.

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/llm-paramiko-network-automation.git
cd llm-paramiko-network-automation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Pull the Ollama model:

```bash
ollama pull llama3.2:1b
```

Ensure the Ollama service is running before executing the script.

## Usage

Run:

```bash
python main.py
```

Example:

```text
Question? Show interface status and routing table on r1 and r2
```

## Example Output

```text
Connecting to r1

R1>show ip interface brief
...

Closing the connection to r1

Connecting to r2

R2>show ip route
...

Closing the connection to r2
```

## Error Handling

Unknown Device:

```text
Unknown device r3
```

Connection Failure:

```text
Failed to connect r2 [WinError 10060]
```

JSON Parsing Failure:

```text
JSON Parsing failed
```

## Lab Environment

This project was developed and tested using Cisco IOS routers running in a GNS3 lab environment.

## Future Enhancements

* Netmiko implementation
* YAML inventory support
* Concurrent device execution
* Command validation
* Configuration deployment support
* Logging
* Nornir integration
* Web interface

## Disclaimer

This project is intended for educational and lab use. Always validate commands before running them on production network devices.
