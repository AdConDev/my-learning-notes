# Definitive Guide: Adding New ESC/POS Commands

This guide provides a complete blueprint for implementing new command structures, their interfaces, tests, and integrations.

### 📋 Implementation Checklist

When adding a new command capability, follow this step-by-step process:

```markdown
## New Command Implementation Checklist

### Phase 1: Design
- [ ] Define the capability interface
- [ ] Design the command structure
- [ ] Identify if it's simple or composite

### Phase 2: Implementation
- [ ] Create the interface definition
- [ ] Implement the concrete struct
- [ ] Add interface compliance check
- [ ] Document all methods

### Phase 3: Testing Infrastructure
- [ ] Create unit tests (`*_test.go`)
- [ ] Create mock implementation (`*_mock_test.go`)
- [ ] Create fake implementation if stateful (`*_fake_test.go`)
- [ ] Add interface composition tests if applicable
- [ ] Add integration tests

### Phase 4: Integration
- [ ] Add to Commands struct
- [ ] Update NewESCPOSProtocol()
- [ ] Create integration tests with Commands
- [ ] Test with dependency injection
```

---

## 🏗️ Step-by-Step Implementation Guide

### Step 1: Define the Interface

**File:** `{capability}_interface.go` or within `{capability}.go`

```go
package escpos

// {Capability}Capability defines the interface for {description}
// Example: BarcodeCapability defines the interface for barcode printing commands
type {Capability}Capability interface {
    // Method names should be descriptive and follow Go conventions
    // Return ([]byte, error) when validation is needed
    // Return []byte for simple command generation
    Method1(param Type) []byte
    Method2(param Type) ([]byte, error)
}

// For composite interfaces (if needed)
type Composite{Capability}Capability interface {
    {Capability}Capability
    Additional{Capability}Capability
}
```

### Step 2: Implement the Concrete Structure

**File:** `{capability}.go`

```go
package escpos

// Interface compliance check - ALWAYS include this
var _ {Capability}Capability = (*{Capability}Commands)(nil)

// {Capability}Commands implements the {Capability}Capability interface
type {Capability}Commands struct {
    // Add fields if stateful
    // For composite: embed other capabilities
    SubCapability SubCapabilityInterface // if needed
}

// Method1 implements a simple command that doesn't require validation
func (c *{Capability}Commands) Method1(param Type) []byte {
    // Build command sequence
    return []byte{ESC, 'X', param}
}

// Method2 implements a command with validation
func (c *{Capability}Commands) Method2(param Type) ([]byte, error) {
    // Validate input
    if param > MaxAllowedValue {
        return nil, errInvalidParameter
    }
    
    // Build command sequence
    return []byte{ESC, 'Y', param}, nil
}
```

### Step 3: Create Unit Tests

**File:** `{capability}_test.go`

```go
package escpos

import (
    "bytes"
    "errors"
    "testing"
)

// Naming Convention: Test{Struct}_{Method}_{Scenario}

// ============================================================================
// {Capability}Commands Tests
// ============================================================================

func Test{Capability}Commands_Method1_ByteSequence(t *testing.T) {
    cmd := &{Capability}Commands{}
    
    tests := []struct {
        name  string
        input Type
        want  []byte
    }{
        {
            name:  "minimum value",
            input: 0,
            want:  []byte{ESC, 'X', 0},
        },
        {
            name:  "typical value", 
            input: 50,
            want:  []byte{ESC, 'X', 50},
        },
        {
            name:  "maximum value",
            input: 255,
            want:  []byte{ESC, 'X', 255},
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := cmd.Method1(tt.input)
            if !bytes.Equal(got, tt.want) {
                t.Errorf("{Capability}Commands.Method1(%v) = %#v, want %#v", 
                    tt.input, got, tt.want)
            }
        })
    }
}

func Test{Capability}Commands_Method2_Validation(t *testing.T) {
    cmd := &{Capability}Commands{}
    
    t.Run("valid range", func(t *testing.T) {
        tests := []struct {
            name  string
            input Type
            want  []byte
        }{
            {
                name:  "minimum valid",
                input: 0,
                want:  []byte{ESC, 'Y', 0},
            },
            {
                name:  "maximum valid",
                input: MaxAllowedValue,
                want:  []byte{ESC, 'Y', MaxAllowedValue},
            },
        }
        
        for _, tt := range tests {
            t.Run(tt.name, func(t *testing.T) {
                got, err := cmd.Method2(tt.input)
                
                if err != nil {
                    t.Errorf("{Capability}Commands.Method2(%v) unexpected error: %v",
                        tt.input, err)
                }
                if !bytes.Equal(got, tt.want) {
                    t.Errorf("{Capability}Commands.Method2(%v) = %#v, want %#v",
                        tt.input, got, tt.want)
                }
            })
        }
    })
    
    t.Run("validation error", func(t *testing.T) {
        input := MaxAllowedValue + 1
        _, err := cmd.Method2(input)
        
        if !errors.Is(err, errInvalidParameter) {
            t.Errorf("{Capability}Commands.Method2(%v) error = %v, want %v",
                input, err, errInvalidParameter)
        }
    })
}
```

### Step 4: Create Mock Implementation

**File:** `{capability}_mock_test.go`

```go
package escpos

import (
    "bytes"
    "testing"
)

// ============================================================================
// Mock Implementation
// ============================================================================

// Mock{Capability}Capability provides a test double for {Capability}Capability
type Mock{Capability}Capability struct {
    // For each method, track:
    // 1. If it was called
    // 2. What input it received
    // 3. What it should return
    
    Method1Called bool
    Method1Input  Type
    Method1Return []byte
    
    Method2Called bool
    Method2Input  Type
    Method2Return []byte
    Method2Error  error
}

// Method1 records the call and returns configured response
func (m *Mock{Capability}Capability) Method1(param Type) []byte {
    m.Method1Called = true
    m.Method1Input = param
    
    if m.Method1Return != nil {
        return m.Method1Return
    }
    // Default behavior
    return []byte{ESC, 'X', byte(param)}
}

// Method2 records the call and returns configured response
func (m *Mock{Capability}Capability) Method2(param Type) ([]byte, error) {
    m.Method2Called = true
    m.Method2Input = param
    
    if m.Method2Error != nil {
        return nil, m.Method2Error
    }
    if m.Method2Return != nil {
        return m.Method2Return, nil
    }
    // Default behavior
    return []byte{ESC, 'Y', byte(param)}, nil
}

// ============================================================================
// Mock Tests
// ============================================================================

func TestMock{Capability}Capability_Method1_BehaviorTracking(t *testing.T) {
    mock := &Mock{Capability}Capability{
        Method1Return: []byte{0xFF, 0xFF}, // Custom response
    }
    
    input := Type(42)
    result := mock.Method1(input)
    
    // Verify tracking
    if !mock.Method1Called {
        t.Error("Mock{Capability}Capability.Method1() should mark Method1Called as true")
    }
    if mock.Method1Input != input {
        t.Errorf("Mock{Capability}Capability.Method1() input = %v, want %v",
            mock.Method1Input, input)
    }
    
    expected := []byte{0xFF, 0xFF}
    if !bytes.Equal(result, expected) {
        t.Errorf("Mock{Capability}Capability.Method1() = %#v, want %#v",
            result, expected)
    }
}

func TestMock{Capability}Capability_Integration_WithCommands(t *testing.T) {
    mock := &Mock{Capability}Capability{}
    
    // Inject mock into Commands
    cmd := &Commands{
        {Capability}: mock,
    }
    
    // Use the command
    input := Type(100)
    result := cmd.{Capability}.Method1(input)
    
    // Verify behavior
    if !mock.Method1Called {
        t.Error("Mock{Capability}Capability.Method1() was not called")
    }
    if mock.Method1Input != input {
        t.Errorf("Mock{Capability}Capability received input %v, want %v",
            mock.Method1Input, input)
    }
    
    // Verify result
    expected := []byte{ESC, 'X', byte(input)}
    if !bytes.Equal(result, expected) {
        t.Errorf("Commands.{Capability}.Method1() = %#v, want %#v",
            result, expected)
    }
}
```

### Step 5: Create Fake Implementation (if stateful)

**File:** `{capability}_fake_test.go`

```go
package escpos

import (
    "bytes"
    "testing"
)

// ============================================================================
// Fake Implementation
// ============================================================================

// Fake{Capability} simulates {capability} with state tracking
type Fake{Capability} struct {
    buffer       []byte
    currentState StateType
    history      []StateType
}

// NewFake{Capability} creates a new fake instance
func NewFake{Capability}() *Fake{Capability} {
    return &Fake{Capability}{
        buffer:       make([]byte, 0),
        currentState: DefaultState,
        history:      make([]StateType, 0),
    }
}

func (f *Fake{Capability}) Method1(param Type) []byte {
    cmd := []byte{ESC, 'X', byte(param)}
    f.buffer = append(f.buffer, cmd...)
    
    // Update state
    f.currentState = StateFromParam(param)
    f.history = append(f.history, f.currentState)
    
    return cmd
}

func (f *Fake{Capability}) Method2(param Type) ([]byte, error) {
    if param > MaxAllowedValue {
        return nil, errInvalidParameter
    }
    
    cmd := []byte{ESC, 'Y', byte(param)}
    f.buffer = append(f.buffer, cmd...)
    
    // Complex state update
    f.currentState = ComplexStateTransition(f.currentState, param)
    f.history = append(f.history, f.currentState)
    
    return cmd, nil
}

// Helper methods for testing
func (f *Fake{Capability}) GetBuffer() []byte {
    return f.buffer
}

func (f *Fake{Capability}) GetState() StateType {
    return f.currentState
}

func (f *Fake{Capability}) GetHistory() []StateType {
    return f.history
}

// ============================================================================
// Fake Implementation Tests
// ============================================================================

func TestFake{Capability}_Method1_StateTracking(t *testing.T) {
    fake := NewFake{Capability}()
    
    // Verify initial state
    if fake.GetState() != DefaultState {
        t.Errorf("Fake{Capability} initial state = %v, want %v",
            fake.GetState(), DefaultState)
    }
    
    // Execute command
    param := Type(42)
    result := fake.Method1(param)
    
    // Verify command generation
    expected := []byte{ESC, 'X', byte(param)}
    if !bytes.Equal(result, expected) {
        t.Errorf("Fake{Capability}.Method1(%v) = %#v, want %#v",
            param, result, expected)
    }
    
    // Verify state change
    expectedState := StateFromParam(param)
    if fake.GetState() != expectedState {
        t.Errorf("Fake{Capability} state after Method1(%v) = %v, want %v",
            param, fake.GetState(), expectedState)
    }
    
    // Verify buffer accumulation
    if !bytes.Contains(fake.GetBuffer(), expected) {
        t.Error("Fake{Capability} buffer should contain command")
    }
    
    // Verify history tracking
    if len(fake.GetHistory()) != 1 {
        t.Errorf("Fake{Capability} history length = %d, want 1",
            len(fake.GetHistory()))
    }
}

func TestFake{Capability}_Integration_ComplexWorkflow(t *testing.T) {
    fake := NewFake{Capability}()
    cmd := &Commands{
        {Capability}: fake,
    }
    
    // Execute a sequence of commands
    workflow := []struct {
        name   string
        action func()
        want   StateType
    }{
        {
            name: "initial setup",
            action: func() {
                cmd.{Capability}.Method1(10)
            },
            want: StateFromParam(10),
        },
        {
            name: "state transition",
            action: func() {
                cmd.{Capability}.Method2(20)
            },
            want: ComplexStateTransition(StateFromParam(10), 20),
        },
    }
    
    for _, step := range workflow {
        t.Run(step.name, func(t *testing.T) {
            step.action()
            
            if fake.GetState() != step.want {
                t.Errorf("After %s, state = %v, want %v",
                    step.name, fake.GetState(), step.want)
            }
        })
    }
    
    // Verify complete history
    if len(fake.GetHistory()) != len(workflow) {
        t.Errorf("History length = %d, want %d",
            len(fake.GetHistory()), len(workflow))
    }
}
```

### Step 6: Interface Composition Tests (if applicable)

**File:** `{capability}_interface_composition_test.go`

```go
package escpos

import (
    "testing"
)

// ============================================================================
// Interface Composition Tests
// ============================================================================

func Test{Capability}Commands_Implements_{Capability}Capability(t *testing.T) {
    cmd := &{Capability}Commands{}
    
    // Verify type implements interface
    var capability {Capability}Capability = cmd
    
    // Test through interface
    result := capability.Method1(TestValue)
    if len(result) == 0 {
        t.Error("{Capability}Capability.Method1() should return non-empty result")
    }
}

// For composite interfaces
func Test{Capability}Commands_Implements_Multiple_Interfaces(t *testing.T) {
    cmd := &{Capability}Commands{}
    
    t.Run("implements {Capability}Capability", func(t *testing.T) {
        var cap1 {Capability}Capability = cmd
        // Test interface methods
        _ = cap1.Method1(TestValue)
    })
    
    t.Run("implements Additional{Capability}Capability", func(t *testing.T) {
        var cap2 Additional{Capability}Capability = cmd
        // Test interface methods
        _ = cap2.AdditionalMethod(TestValue)
    })
    
    t.Run("implements Composite{Capability}Capability", func(t *testing.T) {
        var composite Composite{Capability}Capability = cmd
        // Test all methods are accessible
        _ = composite.Method1(TestValue)
        _ = composite.AdditionalMethod(TestValue)
    })
}

func Test{Capability}_Polymorphism(t *testing.T) {
    cmd := &{Capability}Commands{}
    
    // Function that accepts interface
    processCapability := func(cap {Capability}Capability) bool {
        result := cap.Method1(TestValue)
        return len(result) > 0
    }
    
    // Same struct works through interface
    if !processCapability(cmd) {
        t.Error("{Capability}Commands should work as {Capability}Capability")
    }
}
```

### Step 7: Dependency Injection Tests

**File:** `{capability}_dependency_injection_test.go`

```go
package escpos

import (
    "testing"
)

// ============================================================================
// Helper Functions for Dependency Injection
// ============================================================================

// process{Capability} demonstrates dependency injection
func process{Capability}(cap {Capability}Capability, param Type) ([]byte, error) {
    // Business logic using the capability
    result := cap.Method1(param)
    
    // Additional processing
    additionalResult, err := cap.Method2(param * 2)
    if err != nil {
        return nil, err
    }
    
    // Combine results
    output := append(result, additionalResult...)
    return output, nil
}

// ============================================================================
// Dependency Injection Tests
// ============================================================================

func TestDependencyInjection_Process{Capability}_RealImplementation(t *testing.T) {
    real := &{Capability}Commands{}
    
    output, err := process{Capability}(real, TestValue)
    
    if err != nil {
        t.Fatalf("process{Capability}() unexpected error: %v", err)
    }
    
    // Verify output structure
    minExpectedLen := 6 // Adjust based on your commands
    if len(output) < minExpectedLen {
        t.Errorf("process{Capability}() output length = %d, want >= %d",
            len(output), minExpectedLen)
    }
}

func TestDependencyInjection_Process{Capability}_MockImplementation(t *testing.T) {
    mock := &Mock{Capability}Capability{
        Method1Return: []byte{0x01},
        Method2Return: []byte{0x02},
    }
    
    output, err := process{Capability}(mock, TestValue)
    
    if err != nil {
        t.Fatalf("process{Capability}() unexpected error: %v", err)
    }
    
    // Verify methods were called
    if !mock.Method1Called {
        t.Error("process{Capability}() should call Method1()")
    }
    if !mock.Method2Called {
        t.Error("process{Capability}() should call Method2()")
    }
    
    // Verify correct parameters
    if mock.Method2Input != TestValue*2 {
        t.Errorf("Method2 received %v, want %v",
            mock.Method2Input, TestValue*2)
    }
}

func TestDependencyInjection_SwappableImplementations(t *testing.T) {
    testCases := []struct {
        name    string
        cap     {Capability}Capability
        param   Type
        wantErr bool
    }{
        {
            name:    "real implementation",
            cap:     &{Capability}Commands{},
            param:   ValidValue,
            wantErr: false,
        },
        {
            name:    "mock implementation",
            cap:     &Mock{Capability}Capability{},
            param:   ValidValue,
            wantErr: false,
        },
        {
            name:    "fake implementation",
            cap:     NewFake{Capability}(),
            param:   ValidValue,
            wantErr: false,
        },
        {
            name: "mock with error",
            cap: &Mock{Capability}Capability{
                Method2Error: errInvalidParameter,
            },
            param:   ValidValue,
            wantErr: true,
        },
    }
    
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            _, err := process{Capability}(tc.cap, tc.param)
            
            if (err != nil) != tc.wantErr {
                t.Errorf("process{Capability}() with %s error = %v, wantErr %v",
                    tc.name, err, tc.wantErr)
            }
        })
    }
}
```

### Step 8: Integration with Commands

**File:** `escpos.go` (update existing)

```go
package escpos

// Commands implements the ESC/POS Protocol
type Commands struct {
    Print      PrinterCapability
    LineSpace  LineSpacingCapability
    {Capability} {Capability}Capability  // Add your new capability
}

// NewESCPOSProtocol creates a new instance of the ESC/POS protocol
func NewESCPOSProtocol() *Commands {
    return &Commands{
        Print: &PrintCommands{
            Page: &PagePrint{},
        },
        LineSpace:   &LineSpacingCommands{},
        {Capability}: &{Capability}Commands{},  // Initialize your capability
    }
}
```

**Test File:** `escpos_test.go` (update existing)

```go
func TestNewESCPOSProtocol_Initialization(t *testing.T) {
    cmd := NewESCPOSProtocol()
    
    // ... existing tests ...
    
    // Verify {Capability} is initialized
    if cmd.{Capability} == nil {
        t.Fatal("NewESCPOSProtocol() {Capability} capability should not be nil")
    }
    
    // Verify {Capability} has correct type
    _, ok := cmd.{Capability}.(*{Capability}Commands)
    if !ok {
        t.Error("NewESCPOSProtocol() {Capability} should be of type *{Capability}Commands")
    }
}
```

---

## 📚 Best Practices and Patterns

### Naming Conventions

```go
// Interfaces
type {Noun}Capability interface    // e.g., PrinterCapability, BarcodeCapability

// Concrete implementations
type {Noun}Commands struct          // e.g., PrintCommands, BarcodeCommands

// Test functions
Test{Struct}_{Method}_{Scenario}    // e.g., TestPrintCommands_Text_ValidInput

// Mock types
Mock{Interface}                      // e.g., MockPrinterCapability

// Fake types
Fake{Noun}                          // e.g., FakePrinter

// Test files
{capability}_test.go                 // Unit tests
{capability}_mock_test.go            // Mock implementation
{capability}_fake_test.go            // Fake implementation
{capability}_interface_composition_test.go  // Interface tests
{capability}_dependency_injection_test.go   // DI tests
```

### Error Handling Patterns

```go
// Define errors in constants.go or errors.go
var (
    err{Capability}{Problem} = errors.New("description")
    // e.g., errBarcodeInvalidFormat = errors.New("invalid barcode format")
)

// In implementation
func (c *{Capability}Commands) Method(param Type) ([]byte, error) {
    if !isValid(param) {
        return nil, err{Capability}{Problem}
    }
    return result, nil
}

// In tests
if !errors.Is(err, expectedError) {
    t.Errorf("Method() error = %v, want %v", err, expectedError)
}
```

### Documentation Pattern

```go
// Method implements {interface}.Method
// 
// Format:
//   ASCII: ESC X n
//   Hex:   0x1B 0x58 n
//   Decimal: 27 88 n
//
// Range:
//   n = 0-255
//
// Description:
//   Detailed description of what the command does
//
// Notes:
//   - Important behavior note 1
//   - Important behavior note 2
//
// Byte sequence:
//   ESC X n -> 0x1B, 0x58, n
func (c *{Capability}Commands) Method(n byte) []byte {
    return []byte{ESC, 'X', n}
}
```

### Test Data Patterns

```go
// Use descriptive test case names
tests := []struct {
    name    string
    input   Type
    want    []byte
    wantErr bool
}{
    {
        name:    "minimum value",     // Clear scenario
        input:   0,                    // Edge case
        want:    []byte{ESC, 'X', 0}, // Expected result
        wantErr: false,                // Error expectation
    },
    // ... more cases
}
```

---

## 🎯 Quick Reference Card

### For Simple Commands (like LineSpacing)
1. **Interface**: Single capability, simple methods
2. **Implementation**: Stateless struct
3. **Tests**: Unit, Mock, Integration
4. **No need for**: Fake (unless tracking state), Interface composition

### For Composite Commands (like PrintCommands with Page)
1. **Interface**: Multiple interfaces, composition
2. **Implementation**: Struct with embedded capabilities
3. **Tests**: Unit, Mock, Fake, Interface Composition, Integration
4. **Special attention**: Test all interface paths

### Test Types and When to Use

| Test Type | When to Use | What to Test |
|-----------|------------|--------------|
| **Unit** | Always | Correct byte sequences, validation |
| **Mock** | Always | Behavior tracking, error simulation |
| **Fake** | Stateful operations | State transitions, accumulation |
| **Interface Composition** | Multiple interfaces | Polymorphism, interface compliance |
| **Dependency Injection** | Reusable business logic | Substitutability, flexibility |
| **Integration** | Always | Works with Commands struct |

---

## 🚀 Example: Adding Barcode Capability

Let's apply the guide to add barcode printing:

```go
// Step 1: Interface (barcode.go)
type BarcodeCapability interface {
    PrintBarcode(data string, format BarcodeFormat) ([]byte, error)
    SetBarcodeHeight(n byte) []byte
    SetBarcodeWidth(n byte) []byte
}

// Step 2: Implementation
var _ BarcodeCapability = (*BarcodeCommands)(nil)

type BarcodeCommands struct {
    height byte
    width  byte
}

func (bc *BarcodeCommands) PrintBarcode(data string, format BarcodeFormat) ([]byte, error) {
    if len(data) == 0 {
        return nil, errBarcodeEmptyData
    }
    // Implementation...
    return []byte{GS, 'k', byte(format), byte(len(data))} + []byte(data), nil
}

// Step 3: Tests follow the patterns above...
```

This guide ensures that:
1. **Anyone can continue** your work by following the patterns
2. **Tests are comprehensive** and cover all scenarios
3. **Code is maintainable** with clear structure
4. **Quality is consistent** across all implementations

The key insight from your implementation is that **test organization mirrors code organization** - when code is well-structured with clear interfaces and separation of concerns, the tests naturally follow the same pattern, making the entire codebase more understandable and maintainable.