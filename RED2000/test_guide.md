# Command Implementation Guide

## For Simple Commands (No Composition)

### 1. Define the Capability Interface
```go
// file: capability_name.go
type CapabilityName interface {
    Method1(param type) []byte
    Method2() []byte
}
```

### 2. Create Concrete Implementation
```go
// Add interface compliance check
var _ CapabilityName = (*CommandsStruct)(nil)

type CommandsStruct struct {
    // Add fields if stateful
}

func (cs *CommandsStruct) Method1(param type) []byte {
    // Implementation
    return []byte{/* command bytes */}
}
```

### 3. Create Mock Implementation
```go
// file: mock_test.go
type MockCapabilityName struct {
    Method1Called bool
    Method1Input  type
    Method1Return []byte
    
    Method2Called bool
    Method2Return []byte
}

func (m *MockCapabilityName) Method1(param type) []byte {
    m.Method1Called = true
    m.Method1Input = param
    if m.Method1Return != nil {
        return m.Method1Return
    }
    return []byte{/* default */}
}
```

### 4. Create Tests
```go
// file: capability_name_test.go

// Test 1: Basic functionality
func TestCommandsStruct_Method1(t *testing.T) {
    cs := &CommandsStruct{}
    // Table-driven tests for different inputs
}

// Test 2: Mock behavior
func TestMockCapabilityName(t *testing.T) {
    mock := &MockCapabilityName{}
    // Verify mock tracks calls correctly
}

// Test 3: Integration with Commands
func TestCommands_WithCapabilityName(t *testing.T) {
    // Test with real and mock implementations
}
```

### 5. Add to Commands struct
```go
// file: escpos.go
type Commands struct {
    // ... existing fields
    NewCapability CapabilityName
}

func NewESCPOSProtocol() *Commands {
    return &Commands{
        // ... existing initialization
        NewCapability: &CommandsStruct{},
    }
}
```

## For Composite Commands (With Composition)

### 1. Define Multiple Interfaces
```go
// Sub-capabilities
type SubCapability1 interface {
    SubMethod1() []byte
}

type SubCapability2 interface {
    SubMethod2(param byte) ([]byte, error)
}

// Main capability (composes sub-capabilities)
type MainCapability interface {
    MainMethod() []byte
    // Can embed other capabilities
}
```

### 2. Create Implementations
```go
// Implementation for sub-capability
type SubCommands struct{}

var _ SubCapability1 = (*SubCommands)(nil)
var _ SubCapability2 = (*SubCommands)(nil)

// Main implementation with composition
type MainCommands struct {
    Sub SubCapability1 // or concrete type if appropriate
}

var _ MainCapability = (*MainCommands)(nil)
```

### 3. Additional Tests for Composition
```go
// Test interface composition
func TestInterfaceComposition(t *testing.T) {
    // Verify type can be used as different interfaces
}

// Test that composition works
func TestMainCommands_WithSubCommands(t *testing.T) {
    main := &MainCommands{
        Sub: &SubCommands{},
    }
    // Test interaction between main and sub
}
```

## Testing Checklist

### For ALL Commands:
- [ ] Interface compliance check (`var _ Interface = (*Type)(nil)`)
- [ ] Basic functionality tests (correct byte sequences)
- [ ] Mock implementation and tests
- [ ] Integration test with Commands struct

### Additional for Simple Commands:
- [ ] State tracking test (if stateful)
- [ ] Edge cases (min/max values)

### Additional for Composite Commands:
- [ ] Interface composition test
- [ ] Sub-component interaction test
- [ ] Multiple interface implementation test

## Test Naming Convention

```
Test{StructName}_{MethodName}        // Basic functionality
TestMock{InterfaceName}              // Mock tests
Test{Feature}Integration             // Integration tests
Test{Feature}WithDifferentImplementations  // Polymorphism tests
```

## Assertion Style

Always use consistent assertion messages:
```go
// Good
t.Errorf("MethodName() = %#v, want %#v", got, want)
t.Errorf("MethodName() error = %v, wantErr %v", err, tt.wantErr)

// Include context in complex tests
t.Errorf("MethodName(%d) = %#v, want %#v", input, got, want)
```