import subprocess
import platform
import re

def get_arp_table():
    os_type = platform.system().lower()

    try:
        if os_type == "windows":
            command = ["arp", "-a"]
            pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})"
        else:
            command = ["arp", "-a"]
            pattern = r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]{17})"

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        output = result.stdout
        matches = re.findall(pattern, output)

        print("IP Address        MAC Address")
        print("-----------------------------------")

        count = 0
        results = []

        for ip, mac in matches:
            print(f"{ip:<18}{mac}")
            results.append(f"{ip}    {mac}")
            count += 1

        print("\nTotal entries:", count)

        # Save to file
        choice = input("\nSave results to file? (y/n): ")
        if choice.lower() == "y":
            with open("arp_results.txt", "w") as f:
                f.write("IP Address    MAC Address\n")
                f.write("-----------------------------------\n")
                for line in results:
                    f.write(line + "\n")
                f.write(f"\nTotal entries: {count}\n")

            print("Results saved to arp_results.txt")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    print("=== ARP Scanner ===")
    print("Scanning ARP table...\n")
    get_arp_table()
