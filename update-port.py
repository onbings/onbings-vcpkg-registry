#!/usr/bin/env python3
import argparse
import json
import os.path
import re
import subprocess
import sys
from distutils.version import LooseVersion


VERSION_BASELINE_PATH="versions/baseline.json"
PORTS_DIR_PATH="ports"

class PortNotFound(Exception):
    def __init__(self, port: str, *args: object) -> None:
        super().__init__(*args)
        self.__port = port

    @property
    def message(self) -> str:
        return f"Port '{self.__port}' not found"


class BaselineNotFound(Exception):
    def __init__(self, baseline: str, *args: object) -> None:
        super().__init__(*args)
        self.__baseline = baseline

    @property
    def message(self) -> str:
        return f"Baseline '{self.__baseline}' not found"


class PortNotFoundInBaseline(Exception):
    def __init__(self, port: str, baseline: str, *args: object) -> None:
        super().__init__(*args)
        self.__port = port
        self.__baseline = baseline

    @property
    def message(self) -> str:
        return f"Port '{self.__port}' not found in baseline '{self.__baseline}"

def read_current_port_version(port:str, version:str):
    # Read the current port version for the given version
    # in the version file of the registry
    version_sub_dir = os.path.join("versions", f"{port[0]}-")
    version_path = os.path.join(version_sub_dir, f"{port}.json")
    
    # Version file does not exists (i.e. port have not been added yet)
    if not os.path.isfile(version_path) :
        return -1
        
    with open(version_path, 'r') as f:
        data = json.loads(f.read())

    index = -1
    for i, version_obj in enumerate(data["versions"]):
        if version_obj.get('version', None) == version:
            index = i
            break
            
    # Port exists and version was found        
    if index != -1:
        try:
            # Read current port version
            port_version = data["versions"][index]["port-version"]
        except KeyError:
            # port-version field does not exists. 0 is assumed
            port_version = 0
    # Port exists but version was not found (i.e. new version)
    else:
        port_version = -1
        
    return port_version
    
def update_vcpkg_json(port:str, port_dir: str, version: str) -> None:
    path = os.path.join(port_dir, "vcpkg.json")
    with open(path, 'r') as f:
        data = json.loads(f.read())
    
    # Read the current port version from the version file
    # for the given version
    port_version = read_current_port_version(port, version)
    port_version += 1
    
    # Enforce vcpkg parameters
    data["name"] = port
    data["version"] = version
    data["port-version"] = port_version

    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=2))

def update_portfile(port_dir: str, commit_id: str) -> None:
    path = os.path.join(port_dir, "portfile.cmake")
    with open(path, 'r') as f:
        content = f.read()
    content = re.sub(R"REF\s.*", f"REF {commit_id}", content, count=1)
    with open(path, 'w') as f:
        f.write(content)


def commit(paths: list, message: str = "", amend=False) -> None:
    if not amend:
        print(message)
    add_command = ["git", "add"] + paths
    print(" ".join(add_command))
    subprocess.check_call(add_command)
    commit_command = ["git", "commit"]
    if message:
        commit_command += ["-m", message]
    if amend:
        commit_command.insert(2, "--amend")
        if not message:
            commit_command += ["--no-edit"]
    print(" ".join(commit_command))
    subprocess.check_output(commit_command)


def update_port(port: str, version: str, commit_id: str) -> None:
    port_dir = os.path.join(os.getcwd(), PORTS_DIR_PATH, port)
    if not os.path.exists(port_dir):
        raise PortNotFound(port)

    update_vcpkg_json(port, port_dir, version)
    update_portfile(port_dir, commit_id)
    commit([port_dir], f"Update {port} to {version}/{commit_id}")


def update_port_version(port:str, version:str, path: str):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            f.write(json.dumps({"versions": []}))
    with open(path, 'r') as f:
        data = json.loads(f.read())
    git_tree = subprocess.check_output(["git", "rev-parse", f"HEAD:{PORTS_DIR_PATH}/{port}/"]).decode().splitlines()[0]
    index = -1
    for i, version_obj in enumerate(data["versions"]):
        if version_obj.get('version', None) == version:
            index = i
            break
    if index != -1:
        # update existing version: add new entry with incremented port version
        try:
            port_version = data["versions"][index]["port-version"]
            port_version += 1
        except KeyError:
            port_version = 1
    else:
        port_version = 0

    data["versions"].insert(index, {"version": version, "git-tree": git_tree, "port-version": port_version})
    with open(path, 'w') as f:
        f.write(json.dumps(data, indent=2))
    return port_version   

def update_baseline(baseline_name, port, version, port_version, path=VERSION_BASELINE_PATH):
    with open(path, 'r') as f:
        baselines = json.loads(f.read())
    try:
        baseline = baselines[baseline_name]
    except KeyError:
        raise BaselineNotFound(baseline_name)

    if port in baseline:
        current_version = baseline[port]['baseline']
        if LooseVersion(version) < LooseVersion(current_version):
            print("skipping baseline update, current version is most recent")
            return

    baseline[port] = {"baseline": version, "port-version": port_version}
    baselines[baseline_name] = baseline

    with open(path, 'w') as f:
        f.write(json.dumps(baselines, indent=2))


def update_versions(baseline: str, port: str, version: str, commit_id: str) -> None:
    print(f"Updating baseline: '{baseline}'")
    version_sub_dir = os.path.join("versions", f"{port[0]}-")
    version_path = os.path.join(version_sub_dir, f"{port}.json")
    if not os.path.isdir(version_sub_dir) :
        os.makedirs(version_sub_dir)
    port_version = update_port_version(port, version, version_path)
    update_baseline(baseline, port, version, port_version, path=VERSION_BASELINE_PATH)
    commit([version_path, VERSION_BASELINE_PATH], amend=True)


def fatal(message):
    print(message, file=sys.stderr)
    sys.exit(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    parser.add_argument("version")
    parser.add_argument("commit")
    parser.add_argument("baseline", default="default", nargs='?')
    args = parser.parse_args()

    try:
        update_port(args.port, args.version, args.commit)
        update_versions(args.baseline, args.port, args.version, args.commit)
    except FileNotFoundError as e:
        fatal(f"File not found: {e.filename}")
    except PortNotFound as e:
        fatal(e.message)
    except BaselineNotFound as e:
        fatal(e.message)
    except PortNotFoundInBaseline as e:
        fatal(e.message)


if __name__ == "__main__":
    main()
