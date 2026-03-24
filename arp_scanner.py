import subprocess   # to run system commands
import platform     # to check OS type
import re           # for extracting IP and MAC using regex

def get_arp_table():
    os_type = platform.system().lower()   # getting OS (windows/linux)

    try:
        # setting command and pattern based on OS format
        if os_type == "windows":
            command = ["arp", "-a"]
            pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})"
        else:
            command = ["arp", "-a"]
            pattern = r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]{17})"

        # running arp command
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,   # capture output
            stderr=subprocess.PIPE,
            text=True                # convert output to string
        )

        output = result.stdout   # storing output
        matches = re.findall(pattern, output)   # extracting IP and MAC

        print("IP Address        MAC Address")
        print("-----------------------------------")

        count = 0
        results = []

        # printing all entries
        for ip, mac in matches:
            print(f"{ip:<18}{mac}")
            results.append(f"{ip}    {mac}")   # saving for file
            count += 1

        print("\nTotal entries:", count)

        # asking user to save results
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
        # handling any error
        print("Error:", e)


if __name__ == "__main__":
    print("=== ARP Scanner ===")
    print("Scanning ARP table...\n")
    get_arp_table()
