#!/usr/bin/env python3
"""Test the thinking animation."""

import asyncio
import sys
import time


async def demo_animation():
    """Demonstrate the thinking animation."""

    print("Testing thinking animation...")
    print("=" * 60)

    # Test 1: Simulate thinking then response
    print("\n1. Simulating agent thinking, then responding:")

    thinking_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    # Show thinking animation for 2 seconds
    for i in range(20):
        sys.stdout.write(f"\rAgent: {thinking_chars[i % len(thinking_chars)]} thinking...")
        sys.stdout.flush()
        await asyncio.sleep(0.1)

    # Clear and show response
    sys.stdout.write("\r\033[K")  # Clear line
    sys.stdout.write("Agent: ")
    sys.stdout.flush()

    # Simulate streaming response
    response = "Hello! I'm your Product Owner Agent. How can I help you today?"
    for char in response:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(0.02)

    print("\n")

    # Test 2: Different spinner
    print("2. Alternative animation style:")

    for i in range(20):
        sys.stdout.write(f"\rAgent: {thinking_chars[i % len(thinking_chars)]} processing your request...")
        sys.stdout.flush()
        await asyncio.sleep(0.1)

    sys.stdout.write("\r\033[K")
    sys.stdout.write("Agent: ")
    sys.stdout.flush()

    response = "Analysis complete! ✓"
    for char in response:
        sys.stdout.write(char)
        sys.stdout.flush()
        await asyncio.sleep(0.05)

    print("\n")

    print("=" * 60)
    print("✓ Animation test complete!")


if __name__ == "__main__":
    asyncio.run(demo_animation())