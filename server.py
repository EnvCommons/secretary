from openreward.environments import Server

from env import SecretaryEnvironment

if __name__ == "__main__":
    server = Server([SecretaryEnvironment])
    server.run()
