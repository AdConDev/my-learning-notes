# 📚 The Complete ESC/POS Development Guide

*A step-by-step guide for adding new capabilities to the ESC/POS printer library*

---

## 🎯 Purpose of This Guide

This guide teaches you how to add new printer capabilities (like barcode printing, image handling, or text formatting) to our ESC/POS library. Even if you're new to Go or testing, you'll be able to follow along and contribute quality code.

## 📖 Table of Contents

1. [Understanding the Architecture](#understanding-the-architecture)
2. [Before You Start](#before-you-start)
3. [Complete Tutorial: Adding Barcode Capability](#complete-tutorial-adding-barcode-capability)
4. [Testing Guide](#testing-guide)
5. [Common Mistakes and Solutions](#common-mistakes-and-solutions)
6. [Quick Reference](#quick-reference)

---

## 🏗️ Understanding the Architecture

### What is a "Capability"?

A **capability** is a group of related printer commands. Think of it like a toolbox:

- **Print capability**: Tools for printing text
- **LineSpacing capability**: Tools for controlling line spacing
- **Barcode capability**: Tools for printing barcodes

### The Three Main Parts

Every capability has three parts:

```
┌─────────────────┐
│   INTERFACE     │  ← Defines what methods must exist
├─────────────────┤
│ IMPLEMENTATION  │  ← The actual code that does the work
├─────────────────┤
│     TESTS       │  ← Verifies everything works correctly
└─────────────────┘
```

---

## ✅ Before You Start

### Required Knowledge Checklist

Don't worry if you don't know everything - you can learn as you go!

- [ ] **Basic Go syntax** (variables, functions, structs)
- [ ] **What bytes are** (numbers 0-255 that printers understand)
- [ ] **How to run tests** (`go test ./...`)

### Tools You Need

```bash
# Check if Go is installed
go version

# Your text editor (VS Code recommended)
code .

# Git for version control
git --version
```

---

## 🚀 Complete Tutorial: Adding Barcode Capability

Let's add barcode printing step by step. We'll create files, write code, and test everything.

### 📁 Step 1: Plan Your Files

First, understand what files you'll create:

```
escpos/
├── barcode.go                    # Main implementation
├── barcode_test.go              # Unit tests
├── barcode_mock_test.go         # Mock for testing
├── barcode_fake_test.go         # Fake with state (if needed)
└── constants.go                  # Add constants here
```

### 📝 Step 2: Define Constants and Errors

**File: `constants.go`** (add to existing file)

```go
// ============================================================================
// BARCODE CONSTANTS
// ============================================================================

// BarcodeFormat represents the barcode symbology
type BarcodeFormat byte

const (
    // Barcode formats that printers understand
    BarcodeUPCA   BarcodeFormat = 65  // UPC-A: 11-12 digits
    BarcodeUPCE   BarcodeFormat = 66  // UPC-E: 6 digits
    BarcodeEAN13  BarcodeFormat = 67  // EAN-13: 12-13 digits
    BarcodeEAN8   BarcodeFormat = 68  // EAN-8: 7-8 digits
    BarcodeCode39 BarcodeFormat = 69  // CODE39: variable length
    BarcodeCode128 BarcodeFormat = 73 // CODE128: variable length
)

// Maximum values for barcode parameters
const (
    MaxBarcodeHeight byte = 255  // Maximum height in dots
    MaxBarcodeWidth  byte = 6    // Maximum width multiplier
)

// ============================================================================
// BARCODE ERRORS
// ============================================================================

var (
    // Error messages that explain what went wrong
    errBarcodeEmptyData     = errors.New("barcode data cannot be empty")
    errBarcodeInvalidFormat = errors.New("invalid barcode format")
    errBarcodeInvalidHeight = errors.New("barcode height exceeds maximum")
    errBarcodeInvalidWidth  = errors.New("barcode width exceeds maximum")
    errBarcodeTooLong       = errors.New("barcode data too long for format")
)
```

**Why we need this:**

- Constants give names to magic numbers
- Errors help users understand what went wrong
- Comments explain what each value means

### 🔧 Step 3: Create the Interface

**File: `barcode.go`**

```go
package escpos

// ============================================================================
// BARCODE INTERFACE
// ============================================================================

// BarcodeCapability defines what a barcode printer can do
// This is like a contract - any barcode implementation must have these methods
type BarcodeCapability interface {
    // SetBarcodeHeight sets how tall the barcode will be (in dots)
    // Example: SetBarcodeHeight(100) makes barcodes 100 dots tall
    SetBarcodeHeight(n byte) []byte
    
    // SetBarcodeWidth sets how wide each bar will be (multiplier 1-6)
    // Example: SetBarcodeWidth(2) makes bars twice as wide
    SetBarcodeWidth(n byte) []byte
    
    // PrintBarcode prints actual barcode with given data and format
    // Example: PrintBarcode("123456789012", BarcodeEAN13)
    // Returns error if data is invalid for the format
    PrintBarcode(data string, format BarcodeFormat) ([]byte, error)
    
    // SetBarcodeTextPosition sets where human-readable text appears
    // 0 = no text, 1 = above, 2 = below, 3 = both
    SetBarcodeTextPosition(position byte) []byte
}
```

**Understanding interfaces:**

- An interface is like a job description
- It says "whoever does this job must be able to do X, Y, and Z"
- We can swap different implementations (real printer, mock, fake)

### 🛠️ Step 4: Implement the Interface

Continue in **`barcode.go`**:

```go
// ============================================================================
// BARCODE IMPLEMENTATION
// ============================================================================

// This line checks at compile time that BarcodeCommands implements BarcodeCapability
// If we forget a method, Go will tell us immediately
var _ BarcodeCapability = (*BarcodeCommands)(nil)

// BarcodeCommands implements the BarcodeCapability interface
// This struct holds the actual code that creates barcode commands
type BarcodeCommands struct {
    // Store current settings (optional, for stateful operations)
    currentHeight   byte
    currentWidth    byte
    textPosition    byte
}

// NewBarcodeCommands creates a new barcode command generator with defaults
func NewBarcodeCommands() *BarcodeCommands {
    return &BarcodeCommands{
        currentHeight: 100,  // Default height
        currentWidth:  2,    // Default width
        textPosition:  2,    // Default: text below
    }
}

// SetBarcodeHeight sets the barcode height
//
// Format:
//   ASCII: GS h n
//   Hex:   0x1D 0x68 n
//   Decimal: 29 104 n
//
// Range:
//   n = 1-255 (height in dots)
//
// Default:
//   100 dots (varies by printer model)
//
// Description:
//   Sets the height of the barcode in dots. This affects all subsequent
//   barcodes until changed or printer is reset.
//
// Example:
//   SetBarcodeHeight(150) // Makes barcodes 150 dots tall
//
// Byte sequence:
//   GS h n -> 0x1D, 0x68, n
func (bc *BarcodeCommands) SetBarcodeHeight(n byte) []byte {
    // No validation needed - any byte value is valid
    bc.currentHeight = n  // Remember the setting
    
    // Build the command: GS h n
    return []byte{GS, 'h', n}
}

// SetBarcodeWidth sets the barcode width multiplier
//
// Format:
//   ASCII: GS w n
//   Hex:   0x1D 0x77 n
//   Decimal: 29 119 n
//
// Range:
//   n = 1-6 (width multiplier)
//
// Default:
//   2 (medium width)
//
// Description:
//   Sets the width of barcode bars. 1 = thinnest, 6 = thickest.
//   Affects all subsequent barcodes.
//
// Example:
//   SetBarcodeWidth(3) // Makes bars 3x normal width
//
// Byte sequence:
//   GS w n -> 0x1D, 0x77, n
func (bc *BarcodeCommands) SetBarcodeWidth(n byte) []byte {
    // Width can only be 1-6
    if n < 1 {
        n = 1
    }
    if n > MaxBarcodeWidth {
        n = MaxBarcodeWidth
    }
    
    bc.currentWidth = n
    return []byte{GS, 'w', n}
}

// SetBarcodeTextPosition sets where human-readable text appears
//
// Format:
//   ASCII: GS H n
//   Hex:   0x1D 0x48 n
//   Decimal: 29 72 n
//
// Range:
//   n = 0-3
//   0 = No text
//   1 = Text above barcode
//   2 = Text below barcode
//   3 = Text above and below
//
// Default:
//   0 or 2 (varies by printer)
//
// Byte sequence:
//   GS H n -> 0x1D, 0x48, n
func (bc *BarcodeCommands) SetBarcodeTextPosition(position byte) []byte {
    // Ensure position is 0-3
    if position > 3 {
        position = 2  // Default to below
    }
    
    bc.textPosition = position
    return []byte{GS, 'H', position}
}

// PrintBarcode generates the command to print a barcode
//
// Format:
//   ASCII: GS k m d1...dk (where m is format, k is length)
//   Hex:   0x1D 0x6B m length data...
//
// Parameters:
//   data - The barcode data (numbers/text depending on format)
//   format - The barcode type (EAN13, Code128, etc.)
//
// Returns:
//   Command bytes and error if data is invalid
//
// Example:
//   PrintBarcode("123456789012", BarcodeEAN13)
func (bc *BarcodeCommands) PrintBarcode(data string, format BarcodeFormat) ([]byte, error) {
    // Step 1: Validate input
    if len(data) == 0 {
        return nil, errBarcodeEmptyData
    }
    
    // Step 2: Validate data for specific format
    if err := validateBarcodeData(data, format); err != nil {
        return nil, err
    }
    
    // Step 3: Build command
    // Command structure: GS k format length data...
    dataBytes := []byte(data)
    length := byte(len(dataBytes))
    
    // Create the full command
    cmd := make([]byte, 0, 4+len(dataBytes))
    cmd = append(cmd, GS, 'k', byte(format), length)
    cmd = append(cmd, dataBytes...)
    
    return cmd, nil
}

// validateBarcodeData checks if data is valid for the barcode format
func validateBarcodeData(data string, format BarcodeFormat) error {
    switch format {
    case BarcodeEAN13:
        if len(data) != 13 && len(data) != 12 {
            return errors.New("EAN-13 requires 12 or 13 digits")
        }
        // Check if all characters are digits
        for _, ch := range data {
            if ch < '0' || ch > '9' {
                return errors.New("EAN-13 must contain only digits")
            }
        }
    case BarcodeEAN8:
        if len(data) != 8 && len(data) != 7 {
            return errors.New("EAN-8 requires 7 or 8 digits")
        }
        for _, ch := range data {
            if ch < '0' || ch > '9' {
                return errors.New("EAN-8 must contain only digits")
            }
        }
    case BarcodeCode128:
        // Code128 accepts most ASCII characters
        if len(data) > 253 {  // Typical max length
            return errBarcodeTooLong
        }
    // Add more format validations as needed
    default:
        // For unknown formats, accept any reasonable data
        if len(data) > 253 {
            return errBarcodeTooLong
        }
    }
    return nil
}
```

**Key points for beginners:**

- Each method has detailed documentation
- Validation prevents printer errors
- We store state for complex operations
- Helper functions keep code clean

### 🧪 Step 5: Create Unit Tests

**File: `barcode_test.go`**

```go
package escpos

import (
    "bytes"
    "errors"
    "testing"
)

// ============================================================================
// TEST NAMING CONVENTION: Test{Struct}_{Method}_{Scenario}
// This makes it clear what we're testing
// ============================================================================

// Test simple command generation (no validation needed)
func TestBarcodeCommands_SetBarcodeHeight_ByteSequence(t *testing.T) {
    bc := NewBarcodeCommands()
    
    // Table-driven tests let us test multiple cases easily
    tests := []struct {
        name   string  // Description of the test case
        height byte    // Input value
        want   []byte  // Expected output
    }{
        {
            name:   "minimum height",
            height: 1,
            want:   []byte{GS, 'h', 1},
        },
        {
            name:   "default height",
            height: 100,
            want:   []byte{GS, 'h', 100},
        },
        {
            name:   "maximum height", 
            height: 255,
            want:   []byte{GS, 'h', 255},
        },
    }
    
    // Run each test case
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := bc.SetBarcodeHeight(tt.height)
            
            // Check if output matches expectation
            if !bytes.Equal(got, tt.want) {
                t.Errorf("SetBarcodeHeight(%d) = %#v, want %#v", 
                    tt.height, got, tt.want)
            }
            
            // Also check that state was updated
            if bc.currentHeight != tt.height {
                t.Errorf("currentHeight = %d, want %d", 
                    bc.currentHeight, tt.height)
            }
        })
    }
}

// Test width setting with validation
func TestBarcodeCommands_SetBarcodeWidth_Validation(t *testing.T) {
    bc := NewBarcodeCommands()
    
    tests := []struct {
        name      string
        width     byte
        wantCmd   []byte
        wantState byte  // What width should be stored
    }{
        {
            name:      "minimum width",
            width:     1,
            wantCmd:   []byte{GS, 'w', 1},
            wantState: 1,
        },
        {
            name:      "maximum width",
            width:     6,
            wantCmd:   []byte{GS, 'w', 6},
            wantState: 6,
        },
        {
            name:      "width too small (clamped to 1)",
            width:     0,
            wantCmd:   []byte{GS, 'w', 1},
            wantState: 1,
        },
        {
            name:      "width too large (clamped to 6)",
            width:     10,
            wantCmd:   []byte{GS, 'w', 6},
            wantState: 6,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := bc.SetBarcodeWidth(tt.width)
            
            if !bytes.Equal(got, tt.wantCmd) {
                t.Errorf("SetBarcodeWidth(%d) = %#v, want %#v",
                    tt.width, got, tt.wantCmd)
            }
            
            if bc.currentWidth != tt.wantState {
                t.Errorf("currentWidth = %d, want %d",
                    bc.currentWidth, tt.wantState)
            }
        })
    }
}

// Test barcode printing with various formats
func TestBarcodeCommands_PrintBarcode_ValidInput(t *testing.T) {
    bc := NewBarcodeCommands()
    
    tests := []struct {
        name    string
        data    string
        format  BarcodeFormat
        want    []byte
        wantErr bool
    }{
        {
            name:   "valid EAN-13",
            data:   "123456789012",
            format: BarcodeEAN13,
            want: append(
                []byte{GS, 'k', byte(BarcodeEAN13), 12},
                []byte("123456789012")...,
            ),
            wantErr: false,
        },
        {
            name:   "valid EAN-8",
            data:   "1234567",
            format: BarcodeEAN8,
            want: append(
                []byte{GS, 'k', byte(BarcodeEAN8), 7},
                []byte("1234567")...,
            ),
            wantErr: false,
        },
        {
            name:    "empty data",
            data:    "",
            format:  BarcodeEAN13,
            want:    nil,
            wantErr: true,
        },
        {
            name:    "invalid EAN-13 (letters)",
            data:    "12345678901A",
            format:  BarcodeEAN13,
            want:    nil,
            wantErr: true,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := bc.PrintBarcode(tt.data, tt.format)
            
            // Check error state
            if (err != nil) != tt.wantErr {
                t.Errorf("PrintBarcode(%q, %v) error = %v, wantErr %v",
                    tt.data, tt.format, err, tt.wantErr)
                return
            }
            
            // If no error expected, check the output
            if !tt.wantErr && !bytes.Equal(got, tt.want) {
                t.Errorf("PrintBarcode(%q, %v) = %#v, want %#v",
                    tt.data, tt.format, got, tt.want)
            }
        })
    }
}

// Test error conditions specifically
func TestBarcodeCommands_PrintBarcode_ErrorCases(t *testing.T) {
    bc := NewBarcodeCommands()
    
    t.Run("empty data error", func(t *testing.T) {
        _, err := bc.PrintBarcode("", BarcodeEAN13)
        if !errors.Is(err, errBarcodeEmptyData) {
            t.Errorf("PrintBarcode empty data error = %v, want %v",
                err, errBarcodeEmptyData)
        }
    })
    
    t.Run("invalid EAN-13 length", func(t *testing.T) {
        _, err := bc.PrintBarcode("123", BarcodeEAN13)
        if err == nil {
            t.Error("PrintBarcode should error on invalid EAN-13 length")
        }
    })
    
    t.Run("data too long for Code128", func(t *testing.T) {
        longData := string(make([]byte, 300))  // Too long
        _, err := bc.PrintBarcode(longData, BarcodeCode128)
        if !errors.Is(err, errBarcodeTooLong) {
            t.Errorf("PrintBarcode long data error = %v, want %v",
                err, errBarcodeTooLong)
        }
    })
}
```

**Testing tips for beginners:**

- **Table-driven tests**: Test multiple inputs with one function
- **Test both success and failure**: Make sure errors work too
- **Check state changes**: If your code remembers settings, test them
- **Use descriptive names**: "minimum height" is clearer than "test1"

### 🎭 Step 6: Create Mock Implementation

**File: `barcode_mock_test.go`**

```go
package escpos

import (
    "bytes"
    "testing"
)

// ============================================================================
// MOCK IMPLEMENTATION
// A mock is a fake version used for testing
// It records what methods were called and with what parameters
// ============================================================================

// MockBarcodeCapability is our test double
type MockBarcodeCapability struct {
    // For SetBarcodeHeight
    SetBarcodeHeightCalled bool   // Was the method called?
    SetBarcodeHeightInput  byte   // What parameter was passed?
    SetBarcodeHeightReturn []byte // What should we return?
    
    // For SetBarcodeWidth
    SetBarcodeWidthCalled bool
    SetBarcodeWidthInput  byte
    SetBarcodeWidthReturn []byte
    
    // For SetBarcodeTextPosition
    SetBarcodeTextPositionCalled bool
    SetBarcodeTextPositionInput  byte
    SetBarcodeTextPositionReturn []byte
    
    // For PrintBarcode
    PrintBarcodeCalled bool
    PrintBarcodeData   string
    PrintBarcodeFormat BarcodeFormat
    PrintBarcodeReturn []byte
    PrintBarcodeError  error
}

// Implement the interface methods

func (m *MockBarcodeCapability) SetBarcodeHeight(n byte) []byte {
    // Record that this method was called
    m.SetBarcodeHeightCalled = true
    m.SetBarcodeHeightInput = n
    
    // Return configured response or default
    if m.SetBarcodeHeightReturn != nil {
        return m.SetBarcodeHeightReturn
    }
    return []byte{GS, 'h', n}  // Default behavior
}

func (m *MockBarcodeCapability) SetBarcodeWidth(n byte) []byte {
    m.SetBarcodeWidthCalled = true
    m.SetBarcodeWidthInput = n
    
    if m.SetBarcodeWidthReturn != nil {
        return m.SetBarcodeWidthReturn
    }
    return []byte{GS, 'w', n}
}

func (m *MockBarcodeCapability) SetBarcodeTextPosition(position byte) []byte {
    m.SetBarcodeTextPositionCalled = true
    m.SetBarcodeTextPositionInput = position
    
    if m.SetBarcodeTextPositionReturn != nil {
        return m.SetBarcodeTextPositionReturn
    }
    return []byte{GS, 'H', position}
}

func (m *MockBarcodeCapability) PrintBarcode(data string, format BarcodeFormat) ([]byte, error) {
    m.PrintBarcodeCalled = true
    m.PrintBarcodeData = data
    m.PrintBarcodeFormat = format
    
    // Return configured error if set
    if m.PrintBarcodeError != nil {
        return nil, m.PrintBarcodeError
    }
    
    // Return configured response or default
    if m.PrintBarcodeReturn != nil {
        return m.PrintBarcodeReturn, nil
    }
    
    // Simple default response
    return []byte{GS, 'k', byte(format)}, nil
}

// ============================================================================
// MOCK TESTS
// These tests verify that our mock works correctly
// ============================================================================

func TestMockBarcodeCapability_SetBarcodeHeight_Tracking(t *testing.T) {
    // Create a mock with custom return value
    mock := &MockBarcodeCapability{
        SetBarcodeHeightReturn: []byte{0xFF, 0xFE},  // Custom response
    }
    
    // Call the method
    height := byte(150)
    result := mock.SetBarcodeHeight(height)
    
    // Verify it was tracked
    if !mock.SetBarcodeHeightCalled {
        t.Error("SetBarcodeHeight should be marked as called")
    }
    
    if mock.SetBarcodeHeightInput != height {
        t.Errorf("SetBarcodeHeight input = %d, want %d",
            mock.SetBarcodeHeightInput, height)
    }
    
    // Verify custom response
    expected := []byte{0xFF, 0xFE}
    if !bytes.Equal(result, expected) {
        t.Errorf("SetBarcodeHeight result = %#v, want %#v",
            result, expected)
    }
}

func TestMockBarcodeCapability_PrintBarcode_ErrorSimulation(t *testing.T) {
    // Create mock that simulates an error
    mock := &MockBarcodeCapability{
        PrintBarcodeError: errBarcodeEmptyData,
    }
    
    // Try to print
    _, err := mock.PrintBarcode("123", BarcodeEAN13)
    
    // Verify error was returned
    if !errors.Is(err, errBarcodeEmptyData) {
        t.Errorf("PrintBarcode error = %v, want %v",
            err, errBarcodeEmptyData)
    }
    
    // Verify call was tracked
    if !mock.PrintBarcodeCalled {
        t.Error("PrintBarcode should be marked as called")
    }
}

// Test using mock with Commands struct
func TestMockBarcodeCapability_Integration_WithCommands(t *testing.T) {
    // Create mock
    mock := &MockBarcodeCapability{}
    
    // Inject into Commands
    cmd := &Commands{
        Print:    &PrintCommands{Page: &PagePrint{}},
        LineSpace: &LineSpacingCommands{},
        Barcode:  mock,  // Use our mock
    }
    
    // Use through Commands
    cmd.Barcode.SetBarcodeHeight(100)
    cmd.Barcode.SetBarcodeWidth(3)
    _, _ = cmd.Barcode.PrintBarcode("123456789012", BarcodeEAN13)
    
    // Verify all methods were called
    if !mock.SetBarcodeHeightCalled {
        t.Error("SetBarcodeHeight was not called")
    }
    if !mock.SetBarcodeWidthCalled {
        t.Error("SetBarcodeWidth was not called")
    }
    if !mock.PrintBarcodeCalled {
        t.Error("PrintBarcode was not called")
    }
    
    // Verify correct parameters
    if mock.SetBarcodeHeightInput != 100 {
        t.Errorf("Height = %d, want 100", mock.SetBarcodeHeightInput)
    }
    if mock.PrintBarcodeData != "123456789012" {
        t.Errorf("Barcode data = %q, want %q", 
            mock.PrintBarcodeData, "123456789012")
    }
}
```

**Why mocks are useful:**

- Test without real hardware
- Simulate errors easily
- Verify methods are called correctly
- Test integration with other components

### 🔄 Step 7: Update Main Commands Structure

**File: `escpos.go`** (update existing file)

```go
package escpos

// Commands implements the ESC/POS Protocol
// This is the main entry point for all printer capabilities
type Commands struct {
    Print     PrinterCapability
    LineSpace LineSpacingCapability
    Barcode   BarcodeCapability  // ADD THIS LINE
}

// NewESCPOSProtocol creates a new instance of the ESC/POS protocol
func NewESCPOSProtocol() *Commands {
    return &Commands{
        Print: &PrintCommands{
            Page: &PagePrint{},
        },
        LineSpace: &LineSpacingCommands{},
        Barcode:   NewBarcodeCommands(),  // ADD THIS LINE
    }
}
```

### ✅ Step 8: Add Integration Tests

**File: `escpos_test.go`** (update existing file)

```go
// Add this test to verify barcode is initialized
func TestNewESCPOSProtocol_BarcodeInitialization(t *testing.T) {
    cmd := NewESCPOSProtocol()
    
    // Check barcode capability exists
    if cmd.Barcode == nil {
        t.Fatal("NewESCPOSProtocol() Barcode capability should not be nil")
    }
    
    // Verify correct type
    bc, ok := cmd.Barcode.(*BarcodeCommands)
    if !ok {
        t.Error("Barcode should be of type *BarcodeCommands")
    }
    
    // Verify defaults are set
    if bc.currentHeight != 100 {
        t.Errorf("Default height = %d, want 100", bc.currentHeight)
    }
}

// Integration test: Full barcode printing workflow
func TestCommands_Integration_BarcodePrinting(t *testing.T) {
    cmd := NewESCPOSProtocol()
    
    // Set up barcode parameters
    heightCmd := cmd.Barcode.SetBarcodeHeight(150)
    if len(heightCmd) != 3 {
        t.Errorf("SetBarcodeHeight command length = %d, want 3", 
            len(heightCmd))
    }
    
    widthCmd := cmd.Barcode.SetBarcodeWidth(3)
    if len(widthCmd) != 3 {
        t.Errorf("SetBarcodeWidth command length = %d, want 3", 
            len(widthCmd))
    }
    
    // Print barcode
    barcodeCmd, err := cmd.Barcode.PrintBarcode("123456789012", BarcodeEAN13)
    if err != nil {
        t.Fatalf("PrintBarcode unexpected error: %v", err)
    }
    
    // Verify command structure
    if barcodeCmd[0] != GS || barcodeCmd[1] != 'k' {
        t.Error("Barcode command should start with GS k")
    }
}
```

### 📊 Step 9: Create a Complete Example

**File: `examples/barcode_example.go`** (new file)

```go
package main

import (
    "fmt"
    "log"
    
    "github.com/yourusername/escpos"
)

// This example shows how to use the barcode capability
func main() {
    // Create the ESC/POS command generator
    cmd := escpos.NewESCPOSProtocol()
    
    // Configure barcode appearance
    heightCmd := cmd.Barcode.SetBarcodeHeight(100)
    fmt.Printf("Set height command: %#v\n", heightCmd)
    
    widthCmd := cmd.Barcode.SetBarcodeWidth(2)
    fmt.Printf("Set width command: %#v\n", widthCmd)
    
    textPosCmd := cmd.Barcode.SetBarcodeTextPosition(2)  // Text below
    fmt.Printf("Set text position command: %#v\n", textPosCmd)
    
    // Print different barcode types
    examples := []struct {
        name   string
        data   string
        format escpos.BarcodeFormat
    }{
        {"EAN-13", "123456789012", escpos.BarcodeEAN13},
        {"EAN-8", "1234567", escpos.BarcodeEAN8},
        {"Code 128", "HELLO123", escpos.BarcodeCode128},
    }
    
    for _, ex := range examples {
        barcodeCmd, err := cmd.Barcode.PrintBarcode(ex.data, ex.format)
        if err != nil {
            log.Printf("Error printing %s: %v", ex.name, err)
            continue
        }
        
        fmt.Printf("%s barcode command (%d bytes): %#v\n", 
            ex.name, len(barcodeCmd), barcodeCmd)
    }
    
    // In real usage, you would send these commands to a printer:
    // connector.Write(heightCmd)
    // connector.Write(widthCmd)
    // connector.Write(textPosCmd)
    // connector.Write(barcodeCmd)
}
```

---

## 🧪 Testing Guide

### Understanding Test Types

| Test Type | Purpose | When to Create | Example |
|-----------|---------|----------------|---------|
| **Unit Test** | Tests individual methods | Always | Does `SetHeight(100)` return correct bytes? |
| **Mock Test** | Simulates behavior for testing | Always | Pretend to be a printer, record what happens |
| **Fake Test** | Maintains state across calls | When tracking state | Remember all barcodes printed in a session |
| **Integration Test** | Tests components together | Always | Does barcode work with Commands? |

### Running Your Tests

```bash
# Run all tests
go test ./...

# Run with coverage
go test -cover ./...

# Run specific test
go test -run TestBarcodeCommands_SetBarcodeHeight

# Run with verbose output
go test -v ./...
```

### Test Checklist

Before considering your capability complete:

- [ ] **Unit tests** cover all methods
- [ ] **Error cases** are tested
- [ ] **Edge cases** (min/max values) are tested
- [ ] **Mock** can simulate all behaviors
- [ ] **Integration** with Commands works
- [ ] **Examples** show real usage

---

## ⚠️ Common Mistakes and Solutions

### Mistake 1: Forgetting Interface Compliance Check

❌ **Wrong:**

```go
type BarcodeCommands struct {
    // ...
}
```

✅ **Correct:**

```go
var _ BarcodeCapability = (*BarcodeCommands)(nil)

type BarcodeCommands struct {
    // ...
}
```

**Why:** This line makes Go check at compile time that your struct implements the interface.

### Mistake 2: Not Validating Input

❌ **Wrong:**

```go
func (bc *BarcodeCommands) SetBarcodeWidth(n byte) []byte {
    return []byte{GS, 'w', n}  // What if n > 6?
}
```

✅ **Correct:**

```go
func (bc *BarcodeCommands) SetBarcodeWidth(n byte) []byte {
    if n > MaxBarcodeWidth {
        n = MaxBarcodeWidth  // Clamp to maximum
    }
    return []byte{GS, 'w', n}
}
```

**Why:** Invalid values can cause printer errors or unexpected behavior.

### Mistake 3: Incomplete Error Messages

❌ **Wrong:**

```go
return nil, errors.New("error")
```

✅ **Correct:**

```go
return nil, fmt.Errorf("EAN-13 requires 12-13 digits, got %d", len(data))
```

**Why:** Specific error messages help users fix problems quickly.

### Mistake 4: Missing Documentation

❌ **Wrong:**

```go
func (bc *BarcodeCommands) PrintBarcode(data string, format BarcodeFormat) ([]byte, error) {
    // code...
}
```

✅ **Correct:**

```go
// PrintBarcode generates the command to print a barcode
// 
// Parameters:
//   data - The barcode data (e.g., "123456789012")
//   format - The barcode type (e.g., BarcodeEAN13)
//
// Returns:
//   Command bytes to send to printer, or error if invalid
//
// Example:
//   cmd, err := bc.PrintBarcode("123456789012", BarcodeEAN13)
func (bc *BarcodeCommands) PrintBarcode(data string, format BarcodeFormat) ([]byte, error) {
    // code...
}
```

**Why:** Future developers (including you) need to understand what the code does.

---

## 📚 Quick Reference

### File Naming Convention

```
{capability}.go                    → Implementation
{capability}_test.go              → Unit tests
{capability}_mock_test.go         → Mock for testing
{capability}_fake_test.go         → Stateful fake (optional)
{capability}_integration_test.go  → Integration tests (optional)
```

### Code Structure Pattern

```go
// 1. Interface definition
type {Capability}Capability interface {
    Method1() []byte
    Method2() ([]byte, error)
}

// 2. Compliance check
var _ {Capability}Capability = (*{Capability}Commands)(nil)

// 3. Implementation
type {Capability}Commands struct {
    // fields if needed
}

// 4. Constructor (if needed)
func New{Capability}Commands() *{Capability}Commands {
    return &{Capability}Commands{
        // initialize fields
    }
}

// 5. Methods
func (c *{Capability}Commands) Method1() []byte {
    return []byte{/* command */}
}
```

### Test Naming Pattern

```go
// Format: Test{Struct}_{Method}_{Scenario}

TestBarcodeCommands_SetHeight_ValidInput       // Normal operation
TestBarcodeCommands_SetHeight_EdgeCases        // Min/max values
TestBarcodeCommands_PrintBarcode_ErrorCases    // Error conditions
TestMockBarcode_Integration_WithCommands       // Integration test
```

### Command Documentation Template

```go
// MethodName does X
//
// Format:
//   ASCII: ESC X n
//   Hex:   0x1B 0x58 n
//   Decimal: 27 88 n
//
// Range:
//   n = 0-255
//
// Default:
//   100
//
// Description:
//   Detailed explanation of what this command does
//
// Example:
//   MethodName(50)  // Does X with value 50
//
// Byte sequence:
//   ESC X n -> 0x1B, 0x58, n
func (c *Commands) MethodName(n byte) []byte {
    return []byte{ESC, 'X', n}
}
```

---

## 🎓 Learning Resources

### For Go Beginners

1. **Go Tour**: <https://tour.golang.org/>
2. **Go by Example**: <https://gobyexample.com/>
3. **Effective Go**: <https://golang.org/doc/effective_go>

### For Testing

1. **Go Testing Package**: <https://pkg.go.dev/testing>
2. **Table-Driven Tests**: Search for "golang table driven tests"
3. **Testify (helpful library)**: <https://github.com/stretchr/testify>

### ESC/POS Resources

1. **ESC/POS Command Reference**: Search for "EPSON ESC/POS command reference"
2. **Printer manuals**: Check your printer manufacturer's documentation

---

## 💡 Final Tips

1. **Start small**: Implement one method at a time
2. **Test as you go**: Write tests immediately after each method
3. **Use examples**: Look at existing code (Print, LineSpacing) for patterns
4. **Ask for help**: Comment your code with questions if unsure
5. **Iterate**: Your first version doesn't need to be perfect

Remember: Good tests and documentation are as important as the code itself. They ensure your work can be understood, maintained, and extended by others (including future you).

---

*This guide was created for the ESC/POS library by [@adcondev](https://github.com/adcondev) on 2025-08-27*
