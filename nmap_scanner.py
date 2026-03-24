import subprocess   # to run nmap command
import shutil       # to check if nmap is installed

def check_nmap():
    # checking if nmap exists in system
    if shutil.which("nmap") is None:
        print("Nmap is not installed.")
        return False
    print("Nmap is installed.")
    return True


def run_scan(target, choice):

    # selecting scan type based on user choice
    if choice == "1":
        command = ["nmap", "-sn", target]           # host discovery
    elif choice == "2":
        command = ["nmap", target]                  # default port scan (1–1000)
    elif choice == "3":
        ports = input("Enter port range (example 20-80): ")
        command = ["nmap", "-p", ports, target]     # custom port scan
    elif choice == "4":
        command = ["nmap", "-sV", target]           # service version detection
    elif choice == "5":
        command = ["nmap", "-O", target]            # OS detection
    else:
        print("Invalid choice")
        return

    try:
        print("\nScanning...")

        # running nmap command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,   # capture output
            stderr=subprocess.PIPE,
            text=True,                # convert output to string
            timeout=120               # max time for scan
        )

        print("\nScan Results:\n")
        print(result.stdout)   # printing result

        # asking user to save results
        save = input("Save results to file? (y/n): ")
        if save.lower() == "y":
            with open("nmap_results.txt", "w") as f:
                f.write(result.stdout)
            print("Results saved to nmap_results.txt")

    except subprocess.TimeoutExpired:
        # if scan takes too long
        print("Scan timed out")


if __name__ == "__main__":
    print("=== Nmap Scanner ===")

    # first check if nmap is available
    if check_nmap():

        target = input("Enter target IP or network: ")

        # showing menu
        print("\nSelect scan type:")
        print("1. Basic Host Discovery (-sn)")
        print("2. Port Scan (1-1000)")
        print("3. Custom Port Range Scan")
        print("4. Service Version Detection (-sV)")
        print("5. OS Detection (-O)")

        choice = input("Enter choice (1-5): ")

        run_scan(target, choice)   # calling scan function
