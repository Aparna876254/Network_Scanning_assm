import subprocess
import threading
import csv
from datetime import datetime

results = []

# function to ping a host
def ping_host(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        status = "UP" if result.returncode == 0 else "DOWN"

        # timestamp logging
        time_now = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_now}] {host} is {status}")

        results.append([host, status])

    except:
        print("Error scanning", host)


# scan full network
def scan_network(base_ip):
    threads = []

    for i in range(1, 255):
        ip = base_ip + "." + str(i)

        t = threading.Thread(target=ping_host, args=(ip,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    print("=== Network Scanner ===")

    base_ip = input("Enter base IP (example 192.168.1): ")

    scan_network(base_ip)

    # save to csv
    choice = input("Save results to CSV? (y/n): ")
    if choice.lower() == "y":
        with open("network_results.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "Status"])
            writer.writerows(results)

        print("Saved to network_results.csv")
