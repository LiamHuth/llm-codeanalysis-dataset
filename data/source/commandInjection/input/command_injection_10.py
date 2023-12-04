# author: Liam Huth
# December 2023

import paramiko
import getpass

class RemoteServer:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def evaluate(self, command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=self.hostname, username=self.username, password=self.password)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()

        client.close()
        return output, error

def main():
    hostname = input("Enter the hostname: ")
    username = input("Enter your SSH username: ")
    password = getpass.getpass("Enter your SSH password: ")

    server = RemoteServer(hostname, username, password)

    while True:
        cmd = input("Enter the command to execute (type 'exit' to quit): ")
        if cmd.lower() == 'exit':
            break

        if (cmd[:2] == "rm"):
            print("invalid command")
            continue

        output, error = server.evaluate(cmd)
        if output:
            print(f"Output: {output}")
        if error:
            print(f"Error: {error}")

if __name__ == "__main__":
    main()