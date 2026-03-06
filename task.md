You are implementing a unified API for puncycode (RFC 3492) as a Python uv package.

## Chaos Agent Feature Suggestions

This section tracks enhancement suggestions from the chaos agent during resilience testing.

### Enhancement: Refactor IDNA to_unicode_domain() with Separation of Concerns
- **Category**: Architecture
- **Priority**: Medium
- **Suggested**: 2026-03-06T04:26:50Z
- **Disrupted Unit**: Implement Domain name conversion (IDNA)
- **Why Important**: Currently the validation and decoding logic are tightly coupled in to_unicode_domain(). Separating them would improve testability (validation can be tested independently), allow for validation-only modes, and better follow the single responsibility principle.
- **High-Level Plan**:
  1. Extract domain label validation logic into a separate `validate_domain_labels()` function
  2. Extract domain decoding logic into `decode_domain_labels()` function
  3. Refactor `to_unicode_domain()` to call both functions
  4. Add unit tests for each extracted function
  5. Apply similar refactoring to `to_ascii_domain()` for consistency
- **Status**: Pending

### Enhancement: Optimize Bootstring.adapt() with Lookup Table
- **Category**: Performance
- **Priority**: Medium
- **Suggested**: 2026-03-06T04:30:00Z
- **Disrupted Unit**: Implement Bootstring algorithm core functions
- **Why Important**: The adapt() function is called frequently during encoding/decoding operations for each code point processed. A lookup table approach could significantly reduce computational overhead by avoiding repeated integer divisions and multiplications in the while loop.
- **High-Level Plan**:
  1. Profile current adapt() performance with typical inputs
  2. Analyze the delta range and numpoints patterns in real-world usage
  3. Design a precomputed lookup table for common delta/numpoints combinations
  4. Implement fast-path lookup with fallback to computation for edge cases
  5. Add benchmarks to measure performance improvement
  6. Ensure table accuracy with comprehensive tests
- **Status**: Pending

### Enhancement: Optimize encode() Main Loop Performance
- **Category**: Performance
- **Priority**: High
- **Suggested**: 2026-03-06T04:40:00Z
- **Disrupted Unit**: Implement basic punycode encoding (RFC 3492)
- **Why Important**: The encode() function's main encoding loop processes Unicode strings with nested loops that iterate over input_cp multiple times. For large strings with many non-ASCII characters, this O(n²) behavior can become a bottleneck. Current implementation uses generator expressions and min() inside the loop.
- **High-Level Plan**:
  1. Profile encode() performance with strings of varying lengths (10, 100, 1000+ characters)
  2. Identify hot paths in the encoding loop (likely the min() operation and nested iterations)
  3. Pre-sort or pre-process input_cp to enable more efficient minimum code point finding
  4. Consider using bitmask or bitset operations for encoding deltas
  5. Optimize delta compression using more efficient variable-length integer encoding
  6. Add microbenchmarks to measure improvement for typical use cases
  7. Ensure RFC 3492 compliance with optimized implementation
- **Status**: Pending
