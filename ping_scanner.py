import subprocess
import platform
import re

# Function to ping a single host
def ping_host(host):
    os_type = platform.system().lower()

    if os_type == "windows":
        param = "-n"
    else:
        param = "-c"

    command = ["ping", param, "4", host]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        output = result.stdout

        if result.returncode == 0:
            print("\nHost:", host)
            print("Status: Reachable")

            # Linux average time extraction
            avg_time = re.search(r'rtt min/avg/max/mdev = [\d\.]+/([\d\.]+)/', output)

            if avg_time:
                print("Average Time:", avg_time.group(1), "ms")

        else:
            print("\nHost:", host)
            print("Status: Unreachable")

    except subprocess.TimeoutExpired:
        print("\nHost:", host)
        print("Status: Timeout")


# Function to scan multiple hosts
def scan_multiple_hosts():
    hosts = input("Enter hosts separated by space: ").split()

    for host in hosts:
        ping_host(host)


def main():
    print("=== Ping Scanner ===")

    choice = input("Ping single host? (y/n): ")

    if choice.lower() == 'y':
        host = input("Enter hostname or IP: ")
        ping_host(host)
    else:
        scan_multiple_hosts()


if __name__ == "__main__":
    main()
