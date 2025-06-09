# prune_requirements.py

import pkg_resources
import subprocess
import sys
import os

def get_imported_packages(project_dir):
    """Recursively scan Python files in project_dir for import statements and collect package names."""
    imported = set()
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('import '):
                            parts = line.split()
                            if len(parts) >= 2:
                                imported.add(parts[1].split('.')[0])
                        elif line.startswith('from '):
                            parts = line.split()
                            if len(parts) >= 2:
                                imported.add(parts[1].split('.')[0])
    return imported

def get_requirements_packages(req_file='requirements.txt'):
    """Parse requirements.txt for package names."""
    packages = set()
    with open(req_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name ignoring versions, extras, etc.
                pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                packages.add(pkg.lower())
    return packages

def main(project_dir='.', req_file='requirements.txt'):
    imported_packages = get_imported_packages(project_dir)
    requirements_packages = get_requirements_packages(req_file)

    # Normalize case
    imported_packages = {p.lower() for p in imported_packages}

    print("Packages imported in code but NOT in requirements.txt:")
    for pkg in sorted(imported_packages - requirements_packages):
        print(f"  {pkg}")

    print("\nPackages in requirements.txt but NOT imported in code:")
    for pkg in sorted(requirements_packages - imported_packages):
        print(f"  {pkg}")

    # You can optionally add code here to remove unused packages from requirements.txt after user confirmation

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Check for unused packages in requirements.txt")
    parser.add_argument('--project-dir', default='.', help='Project directory to scan for imports')
    parser.add_argument('--requirements', default='requirements.txt', help='Path to requirements.txt')
    args = parser.parse_args()
    main(args.project_dir, args.requirements)
