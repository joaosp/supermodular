#!/usr/bin/env python3
"""Test message extraction logic."""

from agent import ProductOwnerAgent


def test_message_extraction():
    """Test the _extract_text_from_message method."""
    agent = ProductOwnerAgent()

    # Test 1: String message
    result = agent._extract_text_from_message("Hello, world!")
    assert result == "Hello, world!", f"Expected 'Hello, world!', got '{result}'"
    print("✓ Test 1: String message")

    # Test 2: Dict with text content
    msg_dict = {
        "content": [
            {"type": "text", "text": "This is "},
            {"type": "text", "text": "a test."}
        ]
    }
    result = agent._extract_text_from_message(msg_dict)
    assert result == "This is a test.", f"Expected 'This is a test.', got '{result}'"
    print("✓ Test 2: Dict with text content blocks")

    # Test 3: Dict with direct text
    msg_dict = {"text": "Direct text"}
    result = agent._extract_text_from_message(msg_dict)
    assert result == "Direct text", f"Expected 'Direct text', got '{result}'"
    print("✓ Test 3: Dict with direct text")

    # Test 4: String content
    msg_dict = {"content": "String content"}
    result = agent._extract_text_from_message(msg_dict)
    assert result == "String content", f"Expected 'String content', got '{result}'"
    print("✓ Test 4: String content")

    # Test 5: Tool use message (should be filtered)
    msg_dict = {"subtype": "tool_use", "content": "Some tool data"}
    result = agent._extract_text_from_message(msg_dict)
    assert result == "", f"Expected empty string, got '{result}'"
    print("✓ Test 5: Tool use message filtered")

    # Test 6: Init message (should be filtered)
    msg_dict = {"subtype": "init", "content": "Init data"}
    result = agent._extract_text_from_message(msg_dict)
    assert result == "", f"Expected empty string, got '{result}'"
    print("✓ Test 6: Init message filtered")

    # Test 7: Object with __dict__
    class MessageObj:
        def __init__(self):
            self.content = [{"type": "text", "text": "Object message"}]

    obj = MessageObj()
    result = agent._extract_text_from_message(obj)
    assert result == "Object message", f"Expected 'Object message', got '{result}'"
    print("✓ Test 7: Object with __dict__")

    print("\n" + "=" * 60)
    print("✓ All message extraction tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    test_message_extraction()