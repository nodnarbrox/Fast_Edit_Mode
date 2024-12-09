from output import get_constant_value, DataProcessor

# Test get_constant_value
assert get_constant_value() == 3, "get_constant_value should return 3"

# Test DataProcessor
processor = DataProcessor()
assert processor.value is None, "Initial value should be None"

# Test process_data
test_string = "  hello world  "
result = processor.process_data(test_string)
assert result == "hello world", "process_data should strip whitespace"

print("All tests passed successfully!")
