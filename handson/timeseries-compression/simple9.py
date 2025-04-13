
import numpy as np

"""
Simple9 was proposed in
Inverted Index Compression Using Word-Aligned Binary Codes
VO NGOC ANH, ALISTAIR MOFFAT (2004)
"""


def compress(data):
    """Compress 16-bit integer time series using delta + zig-zag + Simple-9"""
    # Step 1: Delta encoding
    delta = diff_with_prepend(data)
    delta = delta[1:]  # Remove the first element which is just the first value
    
    # Step 2: Zig-zag encoding to make negative numbers positive
    zigzag = [(n << 1) ^ (n >> 15) for n in delta]
    
    # Step 3: Simple-9 encoding
    compressed = simple9_encode(zigzag)
    
    # Add the first value at the beginning for reconstruction
    return [data[0]] + compressed

def decompress(compressed):
    """Decompress data that was compressed with our algorithm"""
    # Extract first value
    first_value = compressed[0]
    
    # Decompress the rest using Simple-9
    zigzag = simple9_decode(compressed[1:])
    
    # Undo zig-zag encoding
    delta = [(n >> 1) ^ (-(n & 1)) for n in zigzag]
    
    # Undo delta encoding
    result = [first_value]
    current = first_value
    for d in delta:
        current += d
        result.append(current)
    
    return result

def diff_with_prepend(data, prepend_value=0):
    # Convert to list to ensure we can index it
    data_list = list(data)
    
    # Create a new list with prepended value
    extended_data = [prepend_value] + data_list
    
    # Calculate differences between consecutive elements
    result = []
    for i in range(1, len(extended_data)):
        result.append(extended_data[i] - extended_data[i-1])
    
    return result

# Simple-9 encoding constants
# Each selector indicates how many bits per integer we use
SIMPLE9_SELECTORS = [
    (1, 28),   # 28 1-bit integers
    (2, 14),   # 14 2-bit integers
    (3, 9),    # 9 3-bit integers
    (4, 7),    # 7 4-bit integers
    (5, 5),    # 5 5-bit integers
    (7, 4),    # 4 7-bit integers
    (9, 3),    # 3 9-bit integers
    (14, 2),   # 2 14-bit integers
    (28, 1)    # 1 28-bit integer
]

def find_selector(values):
    """Find the best selector for a chunk of values"""
    max_val = max(values)
    for bits, count in SIMPLE9_SELECTORS:
        if len(values) <= count and max_val < (1 << bits):
            return bits, count
    raise ValueError(f"Value {max_val} too large for Simple-9 encoding")

def simple9_encode(values):
    """Encode a list of integers using Simple-9 encoding"""
    result = []
    i = 0
    while i < len(values):
        # Find the longest chunk that can be encoded with the same selector
        bits = max_chunk = 0
        for b, c in SIMPLE9_SELECTORS:
            if i + c <= len(values) and max(values[i:i+c]) < (1 << b):
                if c > max_chunk:
                    bits, max_chunk = b, c
        
        if max_chunk == 0:
            # Try to find a selector for a shorter chunk
            remaining = len(values) - i
            chunk = values[i:i+remaining]
            bits, max_chunk = find_selector(chunk)
        
        # Encode chunk
        chunk = values[i:i+max_chunk]
        # Determine selector (4 bits)
        selector = next(idx for idx, (b, c) in enumerate(SIMPLE9_SELECTORS) if b == bits)
        
        # Create the 32-bit word
        word = selector
        shift = 4  # Start after the 4-bit selector
        
        # Pack integers into the word
        for val in chunk:
            word |= (val << shift)
            shift += bits
        
        result.append(word)
        i += max_chunk
    
    return result

def simple9_decode(words):
    """Decode data that was encoded with Simple-9"""
    result = []
    
    for word in words:
        # Extract selector (first 4 bits)
        selector = word & 0xF
        bits, count = SIMPLE9_SELECTORS[selector]
        
        # Extract values
        for i in range(count):
            shift = 4 + i * bits
            mask = (1 << bits) - 1
            val = (word >> shift) & mask
            result.append(val)
    
    return result

# Example usage
if __name__ == "__main__":
    # TODO: add some header
    # format, offset, scaling factor/quantization bits
    # number of series. uint8. Number of (compressed) bytes for each series, int16[s]    

    # Example with synthetic smooth time-series data
    x = np.linspace(0, 6*np.pi, 480)
    original_data = np.round(1000 * np.sin(x)).astype(np.int16)
    
    # Quantize to 10 bits (0-1023)
    quantized = np.clip(original_data // 32 + 512, 0, 1023).tolist()
    
    # Compress
    compressed = compress(quantized)
    
    # Decompress
    decompressed = decompress(compressed)
    
    # Verify correctness
    is_correct = quantized == decompressed
    original_bytes = 2*len(original_data) # 16-bit items
    compressed_bytes = 4*len(compressed) # 32 bit items
    compression_ratio = (original_bytes/compressed_bytes)
    
    print(f"Original length: {original_bytes} bytes")
    print(f"Compressed length: {compressed_bytes} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}x")
    assert is_correct

