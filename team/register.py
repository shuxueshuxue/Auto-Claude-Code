#!/usr/bin/env python3
import json
import os
import sys
import random

NAMES_FILE = "agents.json"

# Cool suffixes - will be shuffled and used globally first
SUFFIXES = [
    "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Neptune", "Pluto",
    "Luna", "Titan", "Europa", "Io", "Callisto", "Ganymede", "Phobos",
    "Orion", "Vega", "Sirius", "Polaris", "Andromeda", "Phoenix"
]

def register_with_role(role):
    """Register an agent with a role-based name"""
    try:
        with open(NAMES_FILE, 'r') as f:
            data = json.load(f)
            taken_names = data.get("registered", [])
            global_suffixes = data.get("global_suffixes", SUFFIXES.copy())
    except FileNotFoundError:
        global_suffixes = SUFFIXES.copy()
        random.shuffle(global_suffixes)
        data = {"registered": [], "global_suffixes": global_suffixes}
        taken_names = []
    
    # Phase 1: Try to use unique global suffix
    if global_suffixes:
        suffix = global_suffixes.pop(0)
        name = f"{role}-{suffix}"
        data["global_suffixes"] = global_suffixes
    else:
        # Phase 2: All global suffixes used, ensure role uniqueness
        same_role_names = [n for n in taken_names if n.startswith(f"{role}-")]
        used_suffixes = [n.split("-", 1)[1] for n in same_role_names if "-" in n]
        
        # Find unused suffix for this role
        available = [s for s in SUFFIXES if s not in used_suffixes]
        
        if available:
            suffix = random.choice(available)
            name = f"{role}-{suffix}"
        else:
            # Last resort - all suffixes used for this role
            name = f"{role}-Star{random.randint(100,999)}"
    
    data["registered"].append(name)
    with open(NAMES_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    return name

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python register.py <role>")
        print("Example: python register.py Designer")
        sys.exit(1)
    
    role = sys.argv[1]
    name = register_with_role(role)
    print(f"Registered as: {name}")
    print(f"Use this name for chat: python chat.py {name} ...")