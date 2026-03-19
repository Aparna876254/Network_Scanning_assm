import subprocess
import shutil

def check_nmap():
    if shutil.which("nmap") is None:
        print("Nmap is not installed.")
        return False
    print("Nmap is installed.")
    return True


def run_scan(target, choice):
    if choice == "1":
        command = ["nmap", "-sn", target]           # Host discovery
    elif choice == "2":
        command = ["nmap", target]                  # Port scan 1–1000
    elif choice == "3":
        ports = input("Enter port range (example 20-80): ")
        command = ["nmap", "-p", ports, target]     # Custom ports
    elif choice == "4":
        command = ["nmap", "-sV", target]           # Service detection
    elif choice == "5":
        command = ["nmap", "-O", target]            # OS detection
    else:
        print("Invalid choice")
        return

    try:
        print("\nScanning...")

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=120
        )

        print("\nScan Results:\n")
        print(result.stdout)

        save = input("Save results to file? (y/n): ")
        if save.lower() == "y":
            with open("nmap_results.txt", "w") as f:
                f.write(result.stdout)
            print("Results saved to nmap_results.txt")

    except subprocess.TimeoutExpired:
        print("Scan timed out")


if __name__ == "__main__":
    print("=== Nmap Scanner ===")

    if check_nmap():

        target = input("Enter target IP or network: ")

        print("\nSelect scan type:")
        print("1. Basic Host Discovery (-sn)")
        print("2. Port Scan (1-1000)")
        print("3. Custom Port Range Scan")
        print("4. Service Version Detection (-sV)")
        print("5. OS Detection (-O)")

        choice = input("Enter choice (1-5): ")

        run_scan(target, choice)
