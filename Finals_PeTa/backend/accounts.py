# Account Manager (file-based)
import os

class AccountManager:
    # Stores accounts in accounts.txt: "username,password"

    def __init__(self, file_path=None):
        if file_path:
            self.file_path = file_path
        else:
            self.file_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "accounts.txt")
            )

        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        except Exception:
            pass

        if not os.path.exists(self.file_path):
            open(self.file_path, "a").close()

    def _read_all(self):
        accounts = {}
        try:
            with open(self.file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if "," in line:
                        u, p = line.split(",", 1)
                    elif ":" in line:
                        u, p = line.split(":", 1)
                    else:
                        continue
                    accounts[u] = p
        except FileNotFoundError:
            pass
        return accounts

    def register(self, username, password):
        username = username.strip()
        password = password.strip()
        if not username or not password:
            return False, "Username and password cannot be empty."

        accounts = self._read_all()
        if username in accounts:
            return False, "Username already exists."

        try:
            with open(self.file_path, "a") as f:
                f.write(f"{username},{password}\n")
        except Exception as e:
            return False, f"Failed to save account: {e}"

        return True, "Registration successful."

    def login(self, username, password):
        accounts = self._read_all()
        if username not in accounts:
            return False, "Account does not exist."
        if accounts[username] != password:
            return False, "Incorrect password."
        return True, "Login successful."

    def exists(self, username):
        return username in self._read_all()
