import yaml

with open("cz.yaml", "r") as stream:
    try:
        print(yaml.safe_load(stream)['commitizen']['version'])
    except yaml.YAMLError as exc:
        print(exc)