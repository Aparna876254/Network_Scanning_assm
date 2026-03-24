import subprocess   # to run system commands like ping
import platform     # to check OS type
import re           # for extracting average time using regex

# Function to ping a single host
def ping_host(host):
    os_type = platform.system().lower()   # get OS (windows/linux/mac)

    # setting parameter based on OS
    if os_type == "windows":
        param = "-n"   # windows uses -n
    else:
        param = "-c"   # linux/mac uses -c

    # forming the ping command
    command = ["ping", param, "4", host]

    try:
        # running the command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,   # capture output
            stderr=subprocess.PIPE,
            text=True,                # output in string format
            timeout=10                # timeout after 10 sec
        )

        output = result.stdout   # store output

        # if ping successful
        if result.returncode == 0:
            print("\nHost:", host)
            print("Status: Reachable")

            # extracting average time (works for linux mostly)
            avg_time = re.search(r'rtt min/avg/max/mdev = [\d\.]+/([\d\.]+)/', output)

            if avg_time:
                print("Average Time:", avg_time.group(1), "ms")

        else:
            print("\nHost:", host)
            print("Status: Unreachable")

    except subprocess.TimeoutExpired:
        # if command takes too long
        print("\nHost:", host)
        print("Status: Timeout")


# Function to scan multiple hosts
def scan_multiple_hosts():
    hosts = input("Enter hosts separated by space: ").split()   # taking multiple inputs

    for host in hosts:
        ping_host(host)   # calling function for each host


def main():
    print("=== Ping Scanner ===")

    choice = input("Ping single host? (y/n): ")

    if choice.lower() == 'y':
        host = input("Enter hostname or IP: ")
        ping_host(host)
    else:
        scan_multiple_hosts()


# starting point of program
if __name__ == "__main__":
    main()
