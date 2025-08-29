# 📚 The Complete ESC/POS Development Guide v2.1

<div align="center">

```text
                    🖨️  ESC/POS MASTERY GUIDE  🖨️                     
                                                                              
  📍 Author: @adcondev                    🏢 Organization: RED 2000           
  📅 Created: July 7, 2025               🔄 Version: 2.1                     
  💻 Environment: Go 1.24.6              🎯 Target: Thermal Printers         
  🌟 Expertise Level: Intermediate       📖 Guide Type: Step-by-Step          
                                                                              
  🚀 "Turning complex printer protocols into simple, testable Go code"        

```

**🔧 Tech Stack:** `Go` • `ESC/POS Protocol` • `Unit Testing` • `Mock/Fake Patterns`

**📋 What You'll Learn:** Interface Design • Package Architecture • Test-Driven Development • Printer Communication

---

</div>

*A step-by-step guide for adding new capabilities to the ESC/POS printer library*

---

## 🎯 Purpose of This Guide

This guide teaches you how to add new printer capabilities to our ESC/POS library following our established architecture. Even if you're new to Go or testing, you'll be able to follow along and contribute quality code.

## 📖 Table of Contents

1. [Understanding the Architecture](#understanding-the-architecture)
2. [Project Structure](#project-structure)
3. [Complete Tutorial: Adding a New Capability](#complete-tutorial-adding-a-new-capability)
4. [Testing Standards](#testing-standards)
5. [Common Mistakes and Solutions](#common-mistakes-and-solutions)
6. [Quick Reference](#quick-reference)

---

## 🏗️ Understanding the Architecture

### Package Organization

Our library is organized into modular packages:

```
escpos/
├── common/          # Shared constants, errors, utilities
├── print/           # Print capability package
├── lineSpacing/     # Line spacing capability package
├── barcode/         # Barcode capability package (example)
└── escpos.go        # Main Commands orchestrator
```

### What is a "Capability"?

A **capability** is a cohesive group of related printer commands, organized as its own package:

- **Print capability**: Commands for printing text and paper control
- **LineSpacing capability**: Commands for controlling line spacing
- **Barcode capability**: Commands for printing barcodes

### The Four Main Components

Every capability package contains:

```
capability/
├── {capability}.go                    # Interface & implementation
├── {capability}_test.go               # Unit tests
├── {capability}_mock_test.go          # Mock implementation
└── {capability}_fake_test.go          # Stateful fake (if needed)
```

---

## 📁 Project Structure

### Current Architecture

```
escpos/
├── common/                             # Shared utilities
│   ├── constants.go                   # ESC/POS byte constants
│   ├── errors.go                       # Common error definitions
│   ├── config.go                       # Configuration constants
│   ├── utils.go                        # Utility functions
│   └── utils_test.go                   # Utility tests
│
├── print/                              # Print capability
│   ├── print.go                        # Interfaces & implementation
│   ├── print_test.go                   # Unit tests
│   ├── print_mock_test.go              # Mock & tests
│   ├── print_fake_test.go              # Fake & tests
│   └── print_interface_composition_test.go  # Interface tests
│
├── lineSpacing/                        # Line spacing capability
│   ├── line_spacing.go                 # Interface & implementation
│   ├── line_spacing_test.go            # Unit tests
│   ├── line_spacing_mock_test.go       # Mock & tests
│   └── line_spacing_fake_test.go       # Fake & tests
│
├── escpos.go                           # Main Commands struct
├── escpos_test.go                      # Commands unit tests
└── escpos_integration_test.go          # Cross-capability integration
```

---

## 🚀 Complete Tutorial: Adding a New Capability

Let's add a barcode printing capability step by step.

### 📝 Step 1: Create the Package Directory

```bash
mkdir escpos/barcode
```

### 📋 Step 2: Define Common Elements

**File: `common/barcode_constants.go`** (new file in common package)

```go
package common

// ============================================================================
// Barcode Constants
// ============================================================================

// BarcodeFormat represents barcode symbology types
type BarcodeFormat byte

const (
    BarcodeUPCA    BarcodeFormat = 65  // UPC-A
    BarcodeUPCE    BarcodeFormat = 66  // UPC-E
    BarcodeEAN13   BarcodeFormat = 67  // EAN-13
    BarcodeEAN8    BarcodeFormat = 68  // EAN-8
    BarcodeCode39  BarcodeFormat = 69  // Code39
    BarcodeCode128 BarcodeFormat = 73  // Code128
)

const (
    MaxBarcodeHeight byte = 255
    MaxBarcodeWidth  byte = 6
)
```

**File: `common/barcode_errors.go`** (new file in common package)

```go
package common

import "errors"

// Barcode-related errors
var (
    ErrBarcodeEmptyData     = errors.New("barcode data cannot be empty")
    ErrBarcodeInvalidFormat = errors.New("invalid barcode format")
    ErrBarcodeInvalidWidth  = errors.New("barcode width exceeds maximum (1-6)")
    ErrBarcodeTooLong       = errors.New("barcode data too long for format")
)
```

### 🔧 Step 3: Create the Capability Interface and Implementation

When creating a capability, consider whether you need sub-structs or interface composition:

**Simple Capability (like linespacing):**

- Single interface
- Single implementation struct
- Direct methods

**Complex Capability with Sub-components (like print):**

- Main interface for common operations
- Sub-structs for grouped functionality (e.g., PagePrint for page-mode operations)
- Expose sub-structs directly on main struct (no nested interfaces)

Example of complex capability structure:

```go
// Main interface - only the commonly used methods
type Capability interface {
    Text(text string) ([]byte, error)
    PrintAndFeedPaper(units byte) []byte
    FormFeed() []byte
    PrintAndCarriageReturn() []byte
    PrintAndLineFeed() []byte
}

// Main implementation with sub-components
type Commands struct {
    Page *PagePrint  // Direct struct, not interface
}

// Sub-component for page mode operations
type PagePrint struct{}

// Methods on sub-component
func (pp *PagePrint) PrintDataInPageMode() []byte { ... }
func (pp *PagePrint) PrintAndReverseFeed(units byte) ([]byte, error) { ... }
```

Usage:

```go
cmd := print.NewCommands()
cmd.Text("Hello")                        // Main capability method
cmd.Page.PrintDataInPageMode()           // Sub-component method
```

### Testing Standards Update

#### Test File Organization

Each capability package must have:

| File | Purpose | Required |
|------|---------|----------|
| `{capability}_test.go` | Unit tests for all structs | ✅ Always |
| `{capability}_mock_test.go` | Mock for main interface | ✅ Always |
| `{capability}_fake_test.go` | Stateful fake | ⚠️ If stateful |

Note: Interface composition tests are no longer needed with the simplified structure.

#### Testing Sub-components

When testing capabilities with sub-components:

1. **Test each struct separately** in the main test file
2. **Group tests by struct** using clear naming:
   - `TestCommands_*` for main struct methods
   - `TestPagePrint_*` for sub-component methods
3. **Mock only the main interface** (sub-components are implementation details)
4. **Fake can track state** across all components if needed

### 🧪 Step 4: Create Unit Tests

**File: `barcode/barcode_test.go`**

```go
package barcode_test

import (
    "bytes"
    "errors"
    "testing"
    
    "github.com/adcondev/pos-printer/escpos/barcode"
    "github.com/adcondev/pos-printer/escpos/common"
)

// Test naming convention: Test{Struct}_{Method}_{Scenario}

func TestCommands_SetBarcodeHeight_ByteSequence(t *testing.T) {
    cmd := barcode.NewCommands()
    
    tests := []struct {
        name   string
        height byte
        want   []byte
    }{
        {
            name:   "minimum height",
            height: 1,
            want:   []byte{common.GS, 'h', 1},
        },
        {
            name:   "default height",
            height: 100,
            want:   []byte{common.GS, 'h', 100},
        },
        {
            name:   "maximum height",
            height: 255,
            want:   []byte{common.GS, 'h', 255},
        },
        {
            name:   "zero becomes minimum",
            height: 0,
            want:   []byte{common.GS, 'h', 1},
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := cmd.SetBarcodeHeight(tt.height)
            if !bytes.Equal(got, tt.want) {
                t.Errorf("SetBarcodeHeight(%d) = %#v, want %#v",
                    tt.height, got, tt.want)
            }
        })
    }
}

func TestCommands_SetBarcodeWidth_Validation(t *testing.T) {
    cmd := barcode.NewCommands()
    
    tests := []struct {
        name  string
        width byte
        want  []byte
    }{
        {
            name:  "minimum width",
            width: 1,
            want:  []byte{common.GS, 'w', 1},
        },
        {
            name:  "maximum width",
            width: 6,
            want:  []byte{common.GS, 'w', 6},
        },
        {
            name:  "zero becomes minimum",
            width: 0,
            want:  []byte{common.GS, 'w', 1},
        },
        {
            name:  "over maximum becomes maximum",
            width: 10,
            want:  []byte{common.GS, 'w', 6},
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := cmd.SetBarcodeWidth(tt.width)
            if !bytes.Equal(got, tt.want) {
                t.Errorf("SetBarcodeWidth(%d) = %#v, want %#v",
                    tt.width, got, tt.want)
            }
        })
    }
}

func TestCommands_PrintBarcode_ValidInput(t *testing.T) {
    cmd := barcode.NewCommands()
    
    tests := []struct {
        name    string
        data    string
        format  common.BarcodeFormat
        wantErr bool
    }{
        {
            name:    "valid EAN-13",
            data:    "123456789012",
            format:  common.BarcodeEAN13,
            wantErr: false,
        },
        {
            name:    "valid EAN-8",
            data:    "1234567",
            format:  common.BarcodeEAN8,
            wantErr: false,
        },
        {
            name:    "empty data",
            data:    "",
            format:  common.BarcodeEAN13,
            wantErr: true,
        },
        {
            name:    "invalid EAN-13 with letters",
            data:    "12345678901A",
            format:  common.BarcodeEAN13,
            wantErr: true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            _, err := cmd.PrintBarcode(tt.data, tt.format)
            if (err != nil) != tt.wantErr {
                t.Errorf("PrintBarcode(%q, %v) error = %v, wantErr %v",
                    tt.data, tt.format, err, tt.wantErr)
            }
        })
    }
}

func TestCommands_PrintBarcode_ErrorCases(t *testing.T) {
    cmd := barcode.NewCommands()
    
    t.Run("empty data error", func(t *testing.T) {
        _, err := cmd.PrintBarcode("", common.BarcodeEAN13)
        if !errors.Is(err, common.ErrBarcodeEmptyData) {
            t.Errorf("PrintBarcode empty data error = %v, want %v",
                err, common.ErrBarcodeEmptyData)
        }
    })
    
    t.Run("invalid EAN-13 length", func(t *testing.T) {
        _, err := cmd.PrintBarcode("123", common.BarcodeEAN13)
        if err == nil {
            t.Error("PrintBarcode should error on invalid EAN-13 length")
        }
    })
}
```

### 🎭 Step 5: Create Mock Implementation

**File: `barcode/barcode_mock_test.go`**

```go
package barcode_test

import (
    "bytes"
    "testing"
    
    "github.com/adcondev/pos-printer/escpos/barcode"
    "github.com/adcondev/pos-printer/escpos/common"
)

// ============================================================================
// Mock Implementation
// ============================================================================

// MockCapability provides a test double for barcode.Capability
type MockCapability struct {
    SetBarcodeHeightCalled bool
    SetBarcodeHeightInput  byte
    SetBarcodeHeightReturn []byte
    
    SetBarcodeWidthCalled bool
    SetBarcodeWidthInput  byte
    SetBarcodeWidthReturn []byte
    
    SetBarcodeTextPositionCalled bool
    SetBarcodeTextPositionInput  byte
    SetBarcodeTextPositionReturn []byte
    
    PrintBarcodeCalled bool
    PrintBarcodeData   string
    PrintBarcodeFormat common.BarcodeFormat
    PrintBarcodeReturn []byte
    PrintBarcodeError  error
}

// Ensure MockCapability implements barcode.Capability
var _ barcode.Capability = (*MockCapability)(nil)

func (m *MockCapability) SetBarcodeHeight(n byte) []byte {
    m.SetBarcodeHeightCalled = true
    m.SetBarcodeHeightInput = n
    
    if m.SetBarcodeHeightReturn != nil {
        return m.SetBarcodeHeightReturn
    }
    return []byte{common.GS, 'h', n}
}

func (m *MockCapability) SetBarcodeWidth(n byte) []byte {
    m.SetBarcodeWidthCalled = true
    m.SetBarcodeWidthInput = n
    
    if m.SetBarcodeWidthReturn != nil {
        return m.SetBarcodeWidthReturn
    }
    return []byte{common.GS, 'w', n}
}

func (m *MockCapability) SetBarcodeTextPosition(position byte) []byte {
    m.SetBarcodeTextPositionCalled = true
    m.SetBarcodeTextPositionInput = position
    
    if m.SetBarcodeTextPositionReturn != nil {
        return m.SetBarcodeTextPositionReturn
    }
    return []byte{common.GS, 'H', position}
}

func (m *MockCapability) PrintBarcode(data string, format common.BarcodeFormat) ([]byte, error) {
    m.PrintBarcodeCalled = true
    m.PrintBarcodeData = data
    m.PrintBarcodeFormat = format
    
    if m.PrintBarcodeError != nil {
        return nil, m.PrintBarcodeError
    }
    if m.PrintBarcodeReturn != nil {
        return m.PrintBarcodeReturn, nil
    }
    return []byte{common.GS, 'k', byte(format)}, nil
}

// ============================================================================
// Mock Tests
// ============================================================================

func TestMockCapability_BehaviorTracking(t *testing.T) {
    t.Run("tracks SetBarcodeHeight calls", func(t *testing.T) {
        mock := &MockCapability{
            SetBarcodeHeightReturn: []byte{0xFF, 0xFE},
        }
        
        result := mock.SetBarcodeHeight(150)
        
        if !mock.SetBarcodeHeightCalled {
            t.Error("SetBarcodeHeight should be marked as called")
        }
        if mock.SetBarcodeHeightInput != 150 {
            t.Errorf("SetBarcodeHeight input = %d, want 150",
                mock.SetBarcodeHeightInput)
        }
        if !bytes.Equal(result, []byte{0xFF, 0xFE}) {
            t.Errorf("SetBarcodeHeight result = %#v, want %#v",
                result, []byte{0xFF, 0xFE})
        }
    })
    
    t.Run("simulates PrintBarcode error", func(t *testing.T) {
        mock := &MockCapability{
            PrintBarcodeError: common.ErrBarcodeEmptyData,
        }
        
        _, err := mock.PrintBarcode("123", common.BarcodeEAN13)
        
        if err != common.ErrBarcodeEmptyData {
            t.Errorf("PrintBarcode error = %v, want %v",
                err, common.ErrBarcodeEmptyData)
        }
        if !mock.PrintBarcodeCalled {
            t.Error("PrintBarcode should be marked as called")
        }
    })
}
```

### 🔧 Step 6: Create Fake Implementation (Optional - for stateful testing)

**File: `barcode/barcode_fake_test.go`**

```go
package barcode_test

import (
    "bytes"
    "testing"
    
    "github.com/adcondev/pos-printer/escpos/barcode"
    "github.com/adcondev/pos-printer/escpos/common"
)

// ============================================================================
// Fake Implementation
// ============================================================================

// FakeCapability simulates barcode printing with state tracking
type FakeCapability struct {
    buffer         []byte
    currentHeight  byte
    currentWidth   byte
    textPosition   byte
    barcodesPrinted int
    lastCommand    string
}

// NewFakeCapability creates a new fake barcode capability
func NewFakeCapability() *FakeCapability {
    return &FakeCapability{
        buffer:        make([]byte, 0),
        currentHeight: 100,
        currentWidth:  2,
        textPosition:  2,
    }
}

// Ensure FakeCapability implements barcode.Capability
var _ barcode.Capability = (*FakeCapability)(nil)

func (f *FakeCapability) SetBarcodeHeight(n byte) []byte {
    if n == 0 {
        n = 1
    }
    cmd := []byte{common.GS, 'h', n}
    f.buffer = append(f.buffer, cmd...)
    f.currentHeight = n
    f.lastCommand = "SetBarcodeHeight"
    return cmd
}

func (f *FakeCapability) SetBarcodeWidth(n byte) []byte {
    if n < 1 {
        n = 1
    }
    if n > 6 {
        n = 6
    }
    cmd := []byte{common.GS, 'w', n}
    f.buffer = append(f.buffer, cmd...)
    f.currentWidth = n
    f.lastCommand = "SetBarcodeWidth"
    return cmd
}

func (f *FakeCapability) SetBarcodeTextPosition(position byte) []byte {
    if position > 3 {
        position = 2
    }
    cmd := []byte{common.GS, 'H', position}
    f.buffer = append(f.buffer, cmd...)
    f.textPosition = position
    f.lastCommand = "SetBarcodeTextPosition"
    return cmd
}

func (f *FakeCapability) PrintBarcode(data string, format common.BarcodeFormat) ([]byte, error) {
    if len(data) == 0 {
        return nil, common.ErrBarcodeEmptyData
    }
    
    dataBytes := []byte(data)
    length := byte(len(dataBytes))
    
    cmd := make([]byte, 0, 4+len(dataBytes))
    cmd = append(cmd, common.GS, 'k', byte(format), length)
    cmd = append(cmd, dataBytes...)
    
    f.buffer = append(f.buffer, cmd...)
    f.barcodesPrinted++
    f.lastCommand = "PrintBarcode"
    
    return cmd, nil
}

// Helper methods
func (f *FakeCapability) GetBuffer() []byte {
    return f.buffer
}

func (f *FakeCapability) GetCurrentHeight() byte {
    return f.currentHeight
}

func (f *FakeCapability) GetBarcodesPrinted() int {
    return f.barcodesPrinted
}

func (f *FakeCapability) Reset() {
    f.buffer = make([]byte, 0)
    f.currentHeight = 100
    f.currentWidth = 2
    f.textPosition = 2
    f.barcodesPrinted = 0
    f.lastCommand = ""
}

// ============================================================================
// Fake Tests
// ============================================================================

func TestFakeCapability_StateTracking(t *testing.T) {
    t.Run("tracks height changes", func(t *testing.T) {
        fake := NewFakeCapability()
        
        fake.SetBarcodeHeight(150)
        
        if fake.GetCurrentHeight() != 150 {
            t.Errorf("CurrentHeight = %d, want 150", fake.GetCurrentHeight())
        }
        if fake.lastCommand != "SetBarcodeHeight" {
            t.Errorf("LastCommand = %q, want %q", fake.lastCommand, "SetBarcodeHeight")
        }
    })
    
    t.Run("counts barcodes printed", func(t *testing.T) {
        fake := NewFakeCapability()
        
        _, _ = fake.PrintBarcode("123456789012", common.BarcodeEAN13)
        _, _ = fake.PrintBarcode("1234567", common.BarcodeEAN8)
        
        if fake.GetBarcodesPrinted() != 2 {
            t.Errorf("BarcodesPrinted = %d, want 2", fake.GetBarcodesPrinted())
        }
    })
    
    t.Run("accumulates buffer", func(t *testing.T) {
        fake := NewFakeCapability()
        
        fake.SetBarcodeHeight(100)
        fake.SetBarcodeWidth(3)
        _, _ = fake.PrintBarcode("123", common.BarcodeCode39)
        
        buffer := fake.GetBuffer()
        
        // Check that all commands are in the buffer
        if !bytes.Contains(buffer, []byte{common.GS, 'h', 100}) {
            t.Error("Buffer should contain height command")
        }
        if !bytes.Contains(buffer, []byte{common.GS, 'w', 3}) {
            t.Error("Buffer should contain width command")
        }
        if !bytes.Contains(buffer, []byte{common.GS, 'k'}) {
            t.Error("Buffer should contain print command")
        }
    })
}
```

### 🔄 Step 7: Update Main Commands Structure

**File: `escpos/escpos.go`**

```go
package escpos

import (
    "github.com/adcondev/pos-printer/escpos/barcode"
    "github.com/adcondev/pos-printer/escpos/common"
    "github.com/adcondev/pos-printer/escpos/lineSpacing"
    "github.com/adcondev/pos-printer/escpos/print"
)

// Commands implements the ESC/POS Protocol
type Commands struct {
    Print     print.Capability
    LineSpace lineSpacing.Capability
    Barcode   barcode.Capability  // ADD THIS
}

// Raw sends raw data without processing
func (c *Commands) Raw(n string) ([]byte, error) {
    if err := common.IsBufOk([]byte(n)); err != nil {
        return nil, err
    }
    return []byte(n), nil
}

// NewEscposProtocol creates a new instance with all capabilities
func NewEscposProtocol() *Commands {
    return &Commands{
        Print: &print.Commands{
            Page: &print.PagePrint{},
        },
        LineSpace: &lineSpacing.Commands{},
        Barcode:   barcode.NewCommands(),  // ADD THIS
    }
}
```

### ✅ Step 8: Add Integration Tests

**File: `escpos/escpos_integration_test.go`** (add to existing)

```go
func TestIntegration_BarcodePrinting(t *testing.T) {
    cmd := escpos.NewEscposProtocol()
    
    // Configure barcode
    heightCmd := cmd.Barcode.SetBarcodeHeight(150)
    if len(heightCmd) != 3 {
        t.Errorf("SetBarcodeHeight command length = %d, want 3", len(heightCmd))
    }
    
    widthCmd := cmd.Barcode.SetBarcodeWidth(3)
    if len(widthCmd) != 3 {
        t.Errorf("SetBarcodeWidth command length = %d, want 3", len(widthCmd))
    }
    
    // Print barcode
    barcodeCmd, err := cmd.Barcode.PrintBarcode("123456789012", common.BarcodeEAN13)
    if err != nil {
        t.Fatalf("PrintBarcode unexpected error: %v", err)
    }
    
    // Verify structure
    if barcodeCmd[0] != common.GS || barcodeCmd[1] != 'k' {
        t.Error("Barcode command should start with GS k")
    }
}
```

---

## 🧪 Testing Standards

### Test Package Naming

Always use `package {capability}_test` for test files:

- Ensures you test only the public API
- Catches accidental exports of internal functions
- Makes tests more realistic

### Test File Organization

Each capability package must have:

| File | Purpose | Required |
|------|---------|----------|
| `{capability}_test.go` | Unit tests | ✅ Always |
| `{capability}_mock_test.go` | Mock implementation | ✅ Always |
| `{capability}_fake_test.go` | Stateful fake | ⚠️ If stateful |
| `{capability}_interface_composition_test.go` | Interface tests | ⚠️ If composite |

### Test Naming Convention

```go
Test{Struct}_{Method}_{Scenario}
```

Examples:

- `TestCommands_SetBarcodeHeight_ByteSequence`
- `TestCommands_PrintBarcode_ErrorCases`
- `TestMockCapability_BehaviorTracking`
- `TestFakeCapability_StateTracking`

### Mock vs Fake Guidelines

**Use Mocks when:**

- Verifying method calls
- Simulating specific returns
- Testing error conditions
- Simple behavior verification

**Use Fakes when:**

- Tracking state changes
- Simulating realistic behavior
- Testing complex workflows
- Verifying accumulated results

### Interface Compliance

Always include compliance checks:

```go
// In implementation file
var _ Capability = (*Commands)(nil)

// In mock test file
var _ barcode.Capability = (*MockCapability)(nil)

// In fake test file
var _ barcode.Capability = (*FakeCapability)(nil)
```

---

## ⚠️ Common Mistakes and Solutions

### Mistake 1: Wrong Package for Tests

❌ **Wrong:**

```go
package barcode  // Same as implementation
```

✅ **Correct:**

```go
package barcode_test  // _test suffix
```

### Mistake 2: Missing Interface Compliance

❌ **Wrong:**

```go
type Commands struct {
    // ...
}
```

✅ **Correct:**

```go
var _ Capability = (*Commands)(nil)

type Commands struct {
    // ...
}
```

### Mistake 3: Duplicate Compliance Checks

❌ **Wrong:**

```go
var _ Capability = (*MockCapability)(nil)
// ... some code ...
var _ Capability = (*MockCapability)(nil)  // Duplicate!
```

✅ **Correct:**

```go
var _ Capability = (*MockCapability)(nil)  // Only once
```

### Mistake 4: Tests in Wrong Location

❌ **Wrong:**

```
escpos/
├── barcode.go
├── barcode_test.go       # Wrong location
└── barcode/
    └── barcode_mock.go   # Split files
```

✅ **Correct:**

```
escpos/
└── barcode/
    ├── barcode.go
    ├── barcode_test.go
    └── barcode_mock_test.go
```

---

## 📚 Quick Reference

### Directory Structure for New Capability

```
escpos/
└── {capability}/
    ├── {capability}.go                    # Interface & implementation
    ├── {capability}_test.go               # Unit tests
    ├── {capability}_mock_test.go          # Mock & tests
    └── {capability}_fake_test.go          # Fake & tests (optional)
```

### Implementation Template

```go
package {capability}

import "github.com/adcondev/pos-printer/escpos/common"

// Interface compliance
var _ Capability = (*Commands)(nil)

// Capability interface
type Capability interface {
    Method1(param byte) []byte
    Method2(param string) ([]byte, error)
}

// Commands implementation
type Commands struct {
    // state fields if needed
}

// NewCommands constructor
func NewCommands() *Commands {
    return &Commands{
        // initialize
    }
}

// Method implementations
func (c *Commands) Method1(param byte) []byte {
    return []byte{common.ESC, 'X', param}
}
```

### Mock Template

```go
package {capability}_test

import "github.com/adcondev/pos-printer/escpos/{capability}"

// MockCapability test double
type MockCapability struct {
    Method1Called bool
    Method1Input  byte
    Method1Return []byte
}

// Interface compliance
var _ {capability}.Capability = (*MockCapability)(nil)

// Method implementations
func (m *MockCapability) Method1(param byte) []byte {
    m.Method1Called = true
    m.Method1Input = param
    if m.Method1Return != nil {
        return m.Method1Return
    }
    return []byte{0x1B, 'X', param}
}
```

### Integration Checklist

When adding a new capability:

- [ ] Create package directory
- [ ] Add constants to `common/`
- [ ] Add errors to `common/`
- [ ] Create interface and implementation
- [ ] Add compliance check
- [ ] Create unit tests with `_test` package
- [ ] Create mock with compliance check
- [ ] Create fake if stateful
- [ ] Update `escpos.Commands` struct
- [ ] Update `NewEscposProtocol()`
- [ ] Add integration tests
- [ ] Run all tests
- [ ] Update documentation

---

## 💡 Final Tips

1. **Package organization**: Keep each capability in its own package
2. **Test package naming**: Always use `package {name}_test`
3. **Compliance checks**: Add them once, at the top
4. **State management**: Use fakes when you need to track state
5. **Documentation**: Every exported function needs comments
6. **Validation**: Always validate inputs to prevent printer errors
7. **Examples**: Create example files to show usage

Remember: The structure is designed for clarity and maintainability. Following these patterns ensures anyone can understand and extend your code.

---

*This guide was created for the ESC/POS library by @adcondev on 2025-07-07*
