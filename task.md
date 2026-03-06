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
