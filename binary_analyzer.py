#!/usr/bin/env python3
"""
Binary Process Analyzer - Terminal Version
Shows beautiful binary patterns in running processes
"""

import subprocess
import sys

def get_running_processes():
    """Get all running processes with their PIDs and commands"""
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = []
        
        for line in result.stdout.split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) > 10:
                    pid = int(parts[1])
                    command = parts[10][:30]
                    user = parts[0]
                    processes.append((pid, command, user))
        
        return processes
    except Exception as e:
        print(f"Error getting processes: {e}")
        return []

def analyze_binary_patterns(processes):
    """Analyze processes for interesting binary patterns"""
    categories = {
        'power_of_2': [],
        'alternating': [],
        'four_ones': [],
        'five_ones': [],
        'six_ones': [],
        'seven_plus_ones': [],
        'palindromes': []
    }
    
    for pid, command, user in processes:
        binary = bin(pid)[2:]  # Remove '0b' prefix
        
        # Power of 2 (only one 1)
        if binary.count('1') == 1:
            categories['power_of_2'].append((pid, binary, command, user))
        
        # Alternating patterns
        if '1010' in binary or '0101' in binary:
            categories['alternating'].append((pid, binary, command, user))
        
        # Consecutive ones patterns
        if '1111' in binary:
            categories['four_ones'].append((pid, binary, command, user))
        if '11111' in binary:
            categories['five_ones'].append((pid, binary, command, user))
        if '111111' in binary:
            categories['six_ones'].append((pid, binary, command, user))
        if '1111111' in binary:
            categories['seven_plus_ones'].append((pid, binary, command, user))
        
        # Palindromes
        if binary == binary[::-1] and len(binary) > 3:
            categories['palindromes'].append((pid, binary, command, user))
    
    return categories

def print_category(title, emoji, processes, max_show=10):
    """Print a category of processes"""
    if not processes:
        return
    
    print(f"\n{emoji} {title.upper()} ({len(processes)} found):")
    print("-" * 60)
    
    for i, (pid, binary, command, user) in enumerate(processes[:max_show]):
        print(f"   PID {pid:<8} = 0b{binary:<20} ({command})")
    
    if len(processes) > max_show:
        print(f"   ... and {len(processes) - max_show} more!")

def main():
    print("🔥 BINARY PROCESS PATTERN ANALYZER 🔥")
    print("=" * 65)
    print("Scanning running processes for beautiful binary patterns...")
    
    processes = get_running_processes()
    if not processes:
        print("No processes found!")
        return
    
    categories = analyze_binary_patterns(processes)
    
    # Show the most interesting categories first
    print_category("Seven or More Consecutive 1s", "👑", categories['seven_plus_ones'], 5)
    print_category("Six Consecutive 1s", "💎", categories['six_ones'], 8)
    print_category("Five Consecutive 1s", "⭐", categories['five_ones'], 10)
    print_category("Palindromic PIDs", "🔄", categories['palindromes'], 10)
    print_category("Power of 2 PIDs", "⚡", categories['power_of_2'], 10)
    print_category("Alternating Patterns", "🎯", categories['alternating'], 10)
    print_category("Four Consecutive 1s", "🌟", categories['four_ones'], 15)
    
    # Summary
    total_interesting = sum(len(cat) for cat in categories.values())
    print(f"\n📊 SUMMARY:")
    print(f"   Total processes scanned: {len(processes)}")
    print(f"   Processes with interesting patterns: {total_interesting}")
    print(f"   Most beautiful: {len(categories['seven_plus_ones'])} with 7+ consecutive 1s")
    
    # Find the biggest PID
    if processes:
        biggest = max(processes, key=lambda x: x[0])
        biggest_binary = bin(biggest[0])[2:]
        print(f"   Biggest PID: {biggest[0]} = 0b{biggest_binary} ({biggest[1]})")

if __name__ == "__main__":
    main()
