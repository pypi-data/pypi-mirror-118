import json


def report(profile: dict):
    print(json.dumps(profile, indent=2))
