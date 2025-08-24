# **Chapter 3: Composite Types**

> *Based on "Learning Go (2nd Edition)"*  
> **Objective**: Deepen your understanding of Go's composite data types—**arrays**, **slices**, **maps**, **structs**, and their intricacies—so you can build flexible and efficient data structures.

---

## **Table of Contents**
1. [Introduction](#introduction)
2. [Arrays](#arrays)
   - [Array Basics](#array-basics)
   - [Array Comparisons](#array-comparisons)
   - [Multidimensional Arrays](#multidimensional-arrays)
3. [Slices](#slices)
   - [Slice Basics](#slice-basics)
   - [Appending to Slices](#appending-to-slices)
   - [Capacity and make](#capacity-and-make)
   - [Slicing Slices](#slicing-slices)
   - [copy Function](#copy-function)
   - [Converting Arrays and Slices](#converting-arrays-and-slices)
4. [Strings, Runes, and Bytes](#strings-runes-and-bytes)
5. [Maps](#maps)
   - [Reading and Writing Maps](#reading-and-writing-maps)
   - [The comma ok Idiom](#the-comma-ok-idiom)
   - [Deleting from Maps](#deleting-from-maps)
   - [Using Maps as Sets](#using-maps-as-sets)
6. [Structs](#structs)
   - [Struct Declarations](#struct-declarations)
   - [Anonymous Structs](#anonymous-structs)
   - [Comparing and Converting Structs](#comparing-and-converting-structs)
7. [Summary and Quick Revision](#summary-and-quick-revision)
   - [Extra Tips](#extra-tips)
   - [Best Practices](#best-practices)
   - [Common Pitfalls](#common-pitfalls)
   - [Interview Questions](#interview-questions)

---

## **Introduction**
In Go, **composite types** help organize complex data into meaningful collections and structures. Each composite type offers unique properties and usage patterns:
- **Arrays**: Fixed-size sequences of elements.
- **Slices**: Flexible, dynamic sequences built on top of arrays.
- **Maps**: Key-value stores for associative data lookups.
- **Structs**: Custom data records with typed fields.
- **Strings** (immutable), **runes** (Unicode code points), and **bytes** (raw data) also interplay in significant ways.

By mastering these, you can optimize your data handling, ensure clarity in your code, and excel in Go-centric interviews.

---

## **Arrays**
### **Array Basics**
- **Definition**: A fixed-length sequence of elements of the same type.
- **Declaration**:
  ```go
  var x [3]int
  x[0] = 10
  x[1] = 20
  x[2] = 30
  ```
- **Literal Initialization**:
  ```go
  var x = [3]int{10, 20, 30}
  var y = [...]int{10, 20, 30} // length inferred
  ```
- **Sparse Array**:
  ```go
  var x = [12]int{1, 5: 4, 6, 10: 100, 15}
  // x => [1 0 0 0 0 4 6 0 0 0 100 15]
  ```
- **Restrictions**:
  - The **array size is part of the type** → cannot be changed at runtime.
  - You **cannot** assign arrays of different lengths to the same variable.
  - Arrays **cannot** be resized; for dynamic behavior, use **slices**.

### **Array Comparisons**
- Arrays are *comparable* with `==` and `!=` if they have the **same length** and element type.
  ```go
  var a = [...]int{10, 20, 30}
  var b = [3]int{10, 20, 30}
  fmt.Println(a == b) // true
  ```
- Elements must match in value and index to be considered equal.

### **Multidimensional Arrays**
- Go doesn’t directly have them, but you can nest arrays:
  ```go
  var matrix [2][3]int
  matrix[0][0] = 1
  ```
- For genuine flexibility, **slices of slices** are more common than fixed two-dimensional arrays.

---

## **Slices**
### **Slice Basics**
- **Definition**: A dynamic, flexible view into an underlying array.
- **Declaration**:
  ```go
  var x []int = []int{10, 20, 30} // slice literal
  var y []int                     // nil slice
  ```
- **Length & Capacity**:
  - `len(x)` → Current number of elements.
  - `cap(x)` → Underlying array capacity for the slice.
- **nil vs. empty**:
  - A **nil** slice (`var x []int`) has `len(x)=0`, `x == nil` is true.
  - An **empty** slice (`y := []int{}`) also has `len(y)=0`, but `y == nil` is false.

### **Appending to Slices**
- Use **append** to grow slices:
  ```go
  x = append(x, 40)         // single value
  x = append(x, 50, 60, 70) // multiple values
  ```
- Append one slice to another:
  ```go
  x = append(x, y...) // y is expanded with ...
  ```
- **Reassignment**: `append` returns a **new slice** which must be reassigned.

### **Capacity and make**
- **make** function for slices:
  ```go
  x := make([]int, 3, 5)
  // length = 3, capacity = 5
  ```
- This pre-allocates a slice with capacity to avoid frequent reallocation during appends.
- `make([]int, 0, 10)` → length 0, capacity 10, not nil.

### **Slicing Slices**
- **Slice expression**: `slice[start:end]`
  ```go
  x := []string{"a", "b", "c", "d"}
  y := x[:2]    // ["a", "b"]
  z := x[1:3]   // ["b", "c"]
  all := x[:]   // ["a", "b", "c", "d"]
  ```
- **Shared memory**: Slicing does not create a copy—changes in one subslice can affect the original.
- **Three-part slice expression** (`start : end : capacity`) can isolate capacity, preventing undesired shared memory after an `append`.

### **copy Function**
- Creates an independent copy of slice elements:
  ```go
  src := []int{1, 2, 3, 4}
  dst := make([]int, 2)
  copy(dst, src[2:])  // copy from the middle
  // dst => [3 4]
  ```
- Returns number of elements copied.

### **Converting Arrays and Slices**
1. **Array → Slice**: `y := xArray[:]`
2. **Slice → Array**: `[4]int(xSlice)` → copies the slice data into the new array.

> **Caution**: Slicing an array shares the same memory. Converting a slice to an array creates a new copy.

---

## **Strings, Runes, and Bytes**
- **Strings** in Go are **immutable**, holding a **sequence of bytes** (UTF-8).
- You can index and slice strings, but remember multi-byte (Unicode) characters.
  ```go
  s := "hello 🤣"
  fmt.Println(len(s))  // length in bytes
  fmt.Println(s[1:4])  // substring -> "ell"
  ```
- **Rune** (`int32`) represents a single Unicode code point.
- **byte** (`uint8`) often used for raw data or ASCII text.
- **Conversions**:
  ```go
  str := "hello 🤣"
  bytes := []byte(str)
  runes := []rune(str)
  ```
  - `bytes` → UTF-8 representation
  - `runes` → Array of code points

---

## **Maps**
- **Definition**: Key-value pairs for associative lookups (hash map under the hood).
- **Declaration**:
  ```go
  var m map[string]int         // nil map
  x := map[string]int{}        // non-nil, empty
  y := map[string]int{"one":1} // literal
  ```
- **len(m)** returns the number of key-value pairs.
- **nil maps** cause a **panic** on writes. Reading a key not in the map → zero value of the value type.

### **Reading and Writing Maps**
```go
myMap := map[string]int{}
myMap["hello"] = 5
myMap["hello"]++       // increment map value
fmt.Println(myMap["hi"]) // 0 (zero value if key not present)
```

### **The comma ok Idiom**
- Distinguish missing keys vs. zero-value keys:
  ```go
  v, ok := myMap["hello"]
  if ok {
    fmt.Println("Key found:", v)
  } else {
    fmt.Println("Key not found")
  }
  ```

### **Deleting from Maps**
```go
delete(myMap, "hello") // removes key "hello"
```

### **Using Maps as Sets**
- Mimic a set by storing keys with a `bool` or empty `struct{}` value:
  ```go
  intSet := map[int]struct{}{}
  intSet[5] = struct{}{}
  _, exists := intSet[5]
  ```

---

## **Structs**
### **Struct Declarations**
- **Definition**: Named collections of fields with types (no inheritance in Go).
  ```go
  type person struct {
      name string
      age  int
  }
  ```
- **Zero Value**: Each field’s zero value (e.g., `""` for strings, `0` for int).
- **Literal Initialization**:
  ```go
  p1 := person{}                   // {"" 0}
  p2 := person{"Alice", 30}        // uses field order
  p3 := person{name: "Bob", age: 20} // named fields
  ```

### **Anonymous Structs**
- Declare a one-off struct type without naming it:
  ```go
  var emp struct {
      name string
      id   int
  }
  emp.name = "Carol"
  emp.id = 42
  ```
- Useful for JSON unmarshaling or quick grouping of data.

### **Comparing and Converting Structs**
- **Comparisons**: Only allowed if all fields are comparable (e.g., no slices or maps).
- **Conversions**: Possible if **two struct types have the same fields, in the same order**.

---

## **Summary and Quick Revision**
1. **Arrays**: Fixed size, rarely used unless size is known at compile time.  
2. **Slices**: Go-to dynamic sequence type with `append`, `len`, and `cap`.  
3. **Strings**: Immutable byte sequences; use `runes` or `[]byte` for advanced manipulation.  
4. **Maps**: Key-value pairs for fast lookups. Remember the comma ok idiom to differentiate zero-value vs. missing keys.  
5. **Structs**: Group fields together into a single entity. Go lacks classes/inheritance, but struct composition is powerful.

### **Extra Tips**
- **Preallocate slices** with `make` if you know approximate size to reduce re-allocations.  
- Use **maps** package (Go 1.21+) for easy map equality checks.  
- Use **slices** package (Go 1.21+) for slice comparisons (`slices.Equal`, `slices.EqualFunc`).  
- **Anonymous structs** can simplify one-off tasks or data transformations.

### **Best Practices**
- **Avoid** slicing unwisely to prevent unintended shared memory—especially when combined with `append`.  
- Always **check** for map key existence with comma ok idiom if zero-values matter.  
- Keep **struct** fields private unless you need external packages to access them.

### **Common Pitfalls**
1. **Forgetting to reassign** from `append(...)`, which returns a new slice reference.  
2. **Writing to a nil map** → runtime panic.  
3. **Confusing array and slice syntax**: `[n]T` vs. `[]T`.  
4. **Ignoring UTF-8** complexities in strings when slicing or indexing.  
5. **Accidentally sharing memory** between slices and arrays or subslices.

### **Interview Questions**
1. **Explain the difference between an array and a slice in Go.**  
   <small>Answer Hint: Discuss fixed length (arrays) vs. dynamic length (slices), types, and typical usage scenarios.</small>  
2. **How do `len` and `cap` differ for slices?**  
   <small>Answer Hint: `len` is the count of elements; `cap` is the underlying array’s size available.</small>  
3. **Why must you explicitly handle reassignments when using `append`?**  
   <small>Answer Hint: `append` can create a new backing array; you must capture the updated slice reference.</small>  
4. **Describe how the comma ok idiom is used with maps.**  
   <small>Answer Hint: Distinguishes missing keys from zero-value keys.</small>  
5. **When would you use an anonymous struct, and why is it useful?**  
   <small>Answer Hint: Quick grouping of fields, often in JSON/protocol unmarshaling, or short-lived data structures.</small>  

---

> **Next Steps**: Practice working with slices and maps under different conditions—especially capacity management and the comma ok idiom. Experiment with struct design to learn how composition replaces class-based inheritance in Go.