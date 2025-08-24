# **Chapter 4: Blocks, Shadows, and Control Structures**

> *Based on "Learning Go (2nd Edition)" – Polished Quick-Reference Guide*  
> **Objective**: Learn how Go organizes code using **blocks**, manage **variable shadowing**, and master Go’s **control structures** (`if`, `for`, `switch`, and even `goto`) for clean, efficient programming.

---

## **Table of Contents**
1. [Introduction](#introduction)  
2. [Blocks & Shadowing](#blocks--shadowing)  
   - [Blocks](#blocks)  
   - [Shadowing Variables](#shadowing-variables)  
   - [The Universe Block](#the-universe-block)  
3. [if Statements](#if-statements)  
4. [for: The Only Loop](#for-the-only-loop)  
   - [Complete (C-style) for](#complete-c-style-for)  
   - [Condition-only for](#condition-only-for)  
   - [Infinite for](#infinite-for)  
   - [break and continue](#break-and-continue)  
   - [for-range](#for-range)  
   - [Labeling for Loops](#labeling-for-loops)  
   - [Choosing the Right for](#choosing-the-right-for)  
5. [switch Statements](#switch-statements)  
   - [Blank Switches](#blank-switches)  
6. [goto Statement](#goto-statement)  
7. [Summary and Quick Revision](#summary-and-quick-revision)  
   - [Extra Tips](#extra-tips)  
   - [Best Practices](#best-practices)  
   - [Common Pitfalls](#common-pitfalls)  
   - [Interview Questions](#interview-questions)

---

## **Introduction**
With the basics of variables, constants, and types behind you, this chapter dives into how Go organizes code within **blocks**, deals with **shadowing** of variables, and uses a handful of **control structures** (`if`, `for`, `switch`, `goto`). While much of this looks similar to C-family languages, Go brings clarity in scoping, eliminates parentheses around conditions, and offers some unique shortcuts.

---

## **Blocks & Shadowing**
### **Blocks**
- **Definition**: A block is any part of the code where **declarations** can occur.  
  - **Package block**: Declaring variables, constants, or types **outside** any function.  
  - **Function-level blocks**: The top level of a function and any nested scopes (e.g., `if` or `for`).  
- Go organizes visibility: **Outer block declarations** are accessible from **inner blocks**, but inner blocks can **override** or **shadow** outer variables.

### **Shadowing Variables**
- **Shadowing**: Occurs when a variable in an **inner block** has the **same name** as one in an **outer block**.
- Can cause confusion if used unintentionally—especially with **`:=`**.
  
  ```go
  func main() {
      x := 10
      if x > 5 {
          x, y := 5, 10
          fmt.Println(x) // 5 (new shadowed x)
      }
      fmt.Println(x)     // 10 (original x)
  }
  ```
> **Tip**: Double-check your usage of `:=` so you don’t accidentally shadow a variable you intended to update.

### **The Universe Block**
- **Outermost block** in Go that contains all **predeclared identifiers**:
  - Built-in types (`int`, `string`, etc.)
  - Built-in functions (`len`, `cap`, `append`, etc.)
  - Constants (`true`, `false`, `iota`)
- Unlike **keywords**, these identifiers are considered part of the **universe block**.

---

## **if Statements**
- Similar to other languages **but**:
  1. **No parentheses** around the condition.
  2. You can **declare** variables in the `if` initializer.

```go
if x := 5; x > 5 {
    fmt.Println("x is greater than 5")
} else {
    fmt.Println("x is less than or equal to 5")
}
```
> Declared variables exist **only** inside the `if`/`else` blocks. Keep this feature for clear, scoped usage.

---

## **for: The Only Loop**
Go has **only one** loop construct: `for`. You can shape it into various forms:

1. **Complete (C-style) for**  
2. **Condition-only for** (like a `while`)  
3. **Infinite for** (like a `while(true)`)  
4. **for-range** (to iterate over arrays, slices, maps, channels, and strings)

### **Complete (C-style) for**
```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```
- No parentheses around condition.
- Initialization and increments are optional.  
- `:=` must be used for initialization (not `var`).
- You can shadow variables if not careful.

### **Condition-only for**
Mimics a **while** loop:
```go
i := 1
for i < 100 {
    fmt.Println(i)
    i *= 2
}
```
No semicolons are used when both initialization and increment are omitted.

### **Infinite for**
Creates an endless loop until a `break` or external interruption:
```go
for {
    fmt.Println("Running forever...")
}
```
> Use **Ctrl + C** to break out when running locally!

### **break and continue**
- **break**: Immediately exits the nearest loop.
- **continue**: Skips to the next iteration of the loop.

```go
for i := 1; i <= 15; i++ {
    if i%3 == 0 && i%5 == 0 {
        fmt.Println("FizzBuzz")
        continue
    }
    if i%3 == 0 {
        fmt.Println("Fizz")
        continue
    }
    if i%5 == 0 {
        fmt.Println("Buzz")
        continue
    }
    fmt.Println(i)
}
```
> This structure shortens if blocks to the minimal body size, improving readability.

### **for-range**
A specialized form to iterate over **collections** like slices, maps, and strings:
```go
numbers := []int{1, 2, 3, 4, 5}
for i, n := range numbers {
    fmt.Println(i, n)
}
```
- First variable: **index** or **key**  
- Second variable: **element** or **value**  

You can **ignore** an unused variable with `_`:
```go
for _, val := range numbers {
    fmt.Println(val)
}
```
> **Order** in a map iteration is **unpredictable**. Go randomizes iteration order to avoid certain DoS attacks.

#### The for-range value is a copy
- Modifying the loop’s value variable **won’t affect** the slice or map.

### **Labeling for Loops**
You can label loops to control **outer** loops in nested scenarios:
```go
outer:
for _, sample := range []string{"hello", "apple_π!"} {
    for i, r := range sample {
        if r == 'l' {
            continue outer
        }
        fmt.Println(i, string(r))
    }
    fmt.Println()
}
```
> The label must be **aligned** with the loop’s braces.

### **Choosing the Right for**
- **for-range**: Default for collections (slices, maps, channels, strings).  
- **Complete for**: When you need an index-based approach with initialization and increment in one place.  
- **Condition-only for**: For loops based on complex conditions (akin to `while`).  
- **Infinite for**: For indefinite loops until `break`, often used in concurrency patterns.

---

## **switch Statements**
Go’s `switch` statement works like a **cleaner** chain of `if-else` checks. No implicit fallthrough (except if explicitly stated).

```go
words := []string{"a", "cow", "smile", "gopher", "octopus", "anthropologist"}
for _, word := range words {
    switch size := len(word); size {
    case 1, 2, 3, 4:
        fmt.Println(word, "is a short word!")
    case 5:
        fmt.Println(word, "is exactly length 5")
    case 6, 7, 8, 9:
        fmt.Println(word, "is a medium-length word!")
    default:
        fmt.Println(word, "is a long word!")
    }
}
```
- **Multiple case** values are supported.
- **Short variable declaration** can scope a variable to the switch.  
- If you need to break out of an outer loop inside a switch, use a **label** on the loop, then `break <label>`.

### **Blank Switches**
- Sometimes called “switch true”; allows for **any boolean comparisons** in `case` blocks:
  ```go
  switch wordLen := len(word); {
  case wordLen < 5:
      fmt.Println(word, "is short")
  case wordLen > 10:
      fmt.Println(word, "is long")
  default:
      fmt.Println(word, "is medium")
  }
  ```
- Replaces messy `if-else if-else` chains with a structured approach.

---

## **goto Statement**
- Allows an **unconditional jump** to a labeled line of code.
- Go restricts usage to avoid skipping variable declarations or jumping into other blocks.

```go
func main() {
    a := 10
    for a < 100 {
        if a%5 == 0 {
            goto done // jump out
        }
        a = a*2 + 1
    }
done:
    fmt.Println("Exited loop, current a:", a)
}
```
> In practice, **goto** is rarely used. It can make code less readable, but occasionally helps handle complex scenarios.

---

## **Summary and Quick Revision**
1. **Blocks**: Nested scopes define variable visibility.  
2. **Shadowing**: Avoid accidental overshadowing of outer variables with `:=`.  
3. **if**: No parentheses; optional variable declarations limited to `if/else` scope.  
4. **for**: The only loop in Go. Use in one of four ways: Complete, Condition-only, Infinite, or for-range.  
5. **switch**: Cleans up multiple comparisons; no implicit fallthrough.  
6. **goto**: Rarely used, but available for special flow control.

### **Extra Tips**
- **Label your loops** carefully for break/continue when nested loops exist.  
- Use **blank switch** statements instead of extensive `if-else if-else`.  
- Keep **if** blocks short and direct (use `continue` in loops to reduce nested ifs).

### **Best Practices**
- Minimize **shadowing**: Be explicit about reusing variable names.  
- Use **for-range** for iterating slices/maps/strings—makes code concise, safer than manual indexing.  
- Use **break/continue** to exit or skip loop iterations early, improving readability.

### **Common Pitfalls**
1. **Shadowing confusion** with `:=` where a developer intends to update an outer variable but accidentally creates a new one.  
2. **Nested loops** without labels can lead to complicated break/continue logic.  
3. **Switch** fallthrough confusion—remember it does not fall through by default in Go.  
4. **goto** used too liberally can become spaghetti code; best used sparingly.

### **Interview Questions**
1. **Explain how variable shadowing works in Go.**  
   <small>Answer Hint: Discuss how an inner scope’s `:=` can overshadow an outer variable with the same name.</small>
2. **Describe the four forms of the Go `for` loop.**  
   <small>Answer Hint: Mention Complete, Condition-only, Infinite, and for-range specifics.</small>
3. **How does `switch` in Go differ from C-style switch statements?**  
   <small>Answer Hint: Emphasize no implicit fallthrough and use of short variable declarations.</small>
4. **When would you consider using a blank switch over if-else statements?**  
   <small>Answer Hint: When multiple boolean conditions are related and you want a cleaner structure.</small>
5. **Is `goto` ever a good idea in Go?**  
   <small>Answer Hint: Rarely; typically for carefully controlling complex loops or early breaks.</small>

---

> **Next Steps**: Build small programs to experiment with variable shadowing and the different `for` styles. Practice `switch` statements and watch out for scope nuances with short declarations. Remember, clarity is key!
