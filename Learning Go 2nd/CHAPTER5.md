# **Chapter 5: Functions**

> *Based on "Learning Go (2nd Edition)" - Polished Quick-Reference Guide*  
> **Objective**: Explore Go's approach to **functions**, including multiple returns, closures, and the `defer` keyword, ensuring you can write clean, idiomatic function code.

---

## **Table of Contents**
1. [Introduction](#introduction)  
2. [Declaring and Calling Functions](#declaring-and-calling-functions)  
   - [Simulating Named and Optional Parameters](#simulating-named-and-optional-parameters)  
   - [Variadic Input Parameters and Slices](#variadic-input-parameters-and-slices)  
3. [Multiple Return Values](#multiple-return-values)  
   - [Ignoring Returned Values](#ignoring-returned-values)  
   - [Named Return Values](#named-return-values)  
   - [Blank Returns—Never Use These!](#blank-returnsnever-use-these)  
4. [Functions as Values](#functions-as-values)  
   - [Function Type Declarations](#function-type-declarations)  
   - [Anonymous Functions](#anonymous-functions)  
   - [Closures](#closures)  
   - [Passing Functions as Parameters](#passing-functions-as-parameters)  
   - [Returning Functions from Functions](#returning-functions-from-functions)  
5. [defer](#defer)  
6. [Go Is Call by Value](#go-is-call-by-value)  
7. [Summary and Quick Revision](#summary-and-quick-revision)  
   - [Extra Tips](#extra-tips)  
   - [Best Practices](#best-practices)  
   - [Common Pitfalls](#common-pitfalls)  
   - [Interview Questions](#interview-questions)

---

## **Introduction**
Go's function model combines familiar C-like structure with unique features like **multiple returns**, **variadic parameters**, and **closures**. This enables concise yet powerful patterns:
- Flexibly handle errors with multiple returns.  
- Pass functions around as **first-class citizens**.  
- Manage cleanup with `defer` to simplify error-prone resource management.

Learning these patterns clarifies how Go programs stay modular, readable, and robust.

---

## **Declaring and Calling Functions**
A basic Go function has:
1. The `func` keyword.  
2. A function **name**.  
3. **Input parameters** with types in parentheses.  
4. An optional **return type** (or multiple types) in parentheses.

```go
func div(num int, denom int) int {
    if denom == 0 {
        return 0
    }
    return num / denom
}

func main() {
    result := div(5, 2)
    fmt.Println(result) // 2
}
```
- **No return type** → no `return` statement needed unless exiting early.
- **Consecutive same-type parameters** can compress type declarations:
  ```go
  func div(num, denom int) int { ... }
  ```

### **Simulating Named and Optional Parameters**
Go lacks **named** and **optional** parameters, but you can simulate them with a **struct**:
```go
type MyFuncOpts struct {
    FirstName string
    LastName  string
    Age       int
}

func MyFunc(opts MyFuncOpts) error {
    // Use opts.FirstName, opts.LastName, opts.Age as needed
    return nil
}

func main() {
    MyFunc(MyFuncOpts{
        LastName: "Patel",
        Age:      50,
    })
}
```
> This pattern clarifies parameters by name and can handle optional fields.

### **Variadic Input Parameters and Slices**
If a function's **last parameter** is declared with `...`, it’s **variadic**. Inside the function, that parameter is a **slice**:
```go
func addTo(base int, vals ...int) []int {
    out := make([]int, 0, len(vals))
    for _, v := range vals {
        out = append(out, base+v)
    }
    return out
}

func main() {
    fmt.Println(addTo(3, 2, 4, 6))   // [5 7 9]
    nums := []int{1, 2, 3}
    fmt.Println(addTo(10, nums...)) // [11 12 13]
}
```
> **Note**: When passing a slice to a variadic parameter, use `sliceName...`.

---

## **Multiple Return Values**
Go functions can return **multiple values**:
```go
func divAndRemainder(num, denom int) (int, int, error) {
    if denom == 0 {
        return 0, 0, errors.New("cannot divide by zero")
    }
    return num / denom, num % denom, nil
}

func main() {
    result, remainder, err := divAndRemainder(5, 2)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(result, remainder) // 2 1
}
```
- Return **all** declared values; you can't group them in parentheses.  
- Convention: **error** is **last** if returning an error condition.

### **Ignoring Returned Values**
If your function returns multiple values but you only need some, you can use `_` to discard:
```go
result, _, err := divAndRemainder(5, 2)
```
If you want to ignore **all** returned values, you can simply call the function without assignment.

### **Named Return Values**
You can name return values in the function signature:
```go
func divAndRemainder(num, denom int) (result, remainder int, err error) {
    if denom == 0 {
        err = errors.New("cannot divide by zero")
        return
    }
    result, remainder = num/denom, num%denom
    return
}
```
- This **predeclares** local variables `result`, `remainder`, and `err`.  
- **Blank returns** (`return` without values) use these predeclared variables.  
- **Shadowing** pitfalls: if you do `result :=` inside the function, you might be creating a new variable rather than assigning to the named return.

### **Blank Returns—Never Use These!**
A **blank return** (`return` with no arguments) can be confusing:
```go
func divAndRemainder(num, denom int) (result, remainder int, err error) {
    if denom == 0 {
        err = errors.New("cannot divide by zero")
        return // returns (0,0,error)
    }
    result, remainder = num/denom, num%denom
    return // returns the named variables
}
```
> Considered **bad practice**. It obscures the actual returned values.

---

## **Functions as Values**
Functions have types determined by their **parameter** and **return** signatures. For example, `func(string) int` matches any function that takes a `string` and returns an `int`.

```go
func f1(a string) int {
    return len(a)
}
func f2(a string) int {
    total := 0
    for _, v := range a {
        total += int(v)
    }
    return total
}

func main() {
    var myFuncVariable func(string) int
    myFuncVariable = f1
    fmt.Println(myFuncVariable("golang")) // 6

    myFuncVariable = f2
    fmt.Println(myFuncVariable("golang")) // 609
}
```
> The **zero value** of a function variable is `nil`. Calling a nil function variable causes a panic.

### **Function Type Declarations**
Create an alias for function signatures:
```go
type MyFuncType func(string) int
```
Any function with `func(string) int` can be assigned to `MyFuncType`.

### **Anonymous Functions**
You can declare a **function without a name** directly:

```go
func main() {
    f := func(j int) {
        fmt.Println("printing", j, "from inside an anonymous function")
    }
    for i := 0; i < 3; i++ {
        f(i)
    }
}
```
- Anonymous functions can be **called immediately**:
  ```go
  func main() {
      for i := 0; i < 3; i++ {
          func(j int) {
              fmt.Println("printing", j, "inline")
          }(i) // call with argument
      }
  }
  ```
- You can define package-level variables assigned to anonymous functions, but this can cause confusion if reassigned at runtime.

### **Closures**
A closure is a function **defined inside another function**, capturing and modifying outer variables:
```go
func main() {
    a := 20
    f := func() {
        fmt.Println(a) // reads outer 'a'
        a = 30         // modifies outer 'a'
    }
    f()
    fmt.Println(a) // 30
}
```
- If you accidentally use `:=`, you **shadow** the outer variable instead of modifying it.

### **Passing Functions as Parameters**
Because functions are **first-class** citizens, you can pass them as parameters. A common scenario is sorting with a custom compare function:

```go
type Person struct {
    FirstName string
    LastName  string
    Age       int
}

people := []Person{
    {"Patel", "Joe", 50},
    {"Smith", "Jane", 30},
    {"Jones", "Chris", 35},
}

func main() {
    // sort by LastName
    sort.Slice(people, func(i, j int) bool {
        return people[i].LastName < people[j].LastName
    })
    fmt.Println(people)
}
```

### **Returning Functions from Functions**
You can **return** a function that closes over local variables:

```go
func makeMult(base int) func(int) int {
    return func(factor int) int {
        return base * factor
    }
}

func main() {
    timesTwo := makeMult(2)
    timesThree := makeMult(3)
    fmt.Println(timesTwo(4), timesThree(4)) // 8 12
}
```
> This pattern is often described as a **higher-order function**.

---

## **defer**
Use `defer` to schedule a function call that executes when the **surrounding function** returns—ideal for cleanup:

```go
func main() {
    f, err := os.Open("data.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer f.Close()

    data := make([]byte, 2048)
    for {
        count, err := f.Read(data)
        if err != nil && err != io.EOF {
            log.Fatal(err)
        }
        if count == 0 {
            break
        }
        os.Stdout.Write(data[:count])
    }
}
```
- **Multiple `defer`s**: executed in **LIFO** order.  
- Arguments to a deferred function are **evaluated immediately**, but the function runs later.  
- You can even combine `defer` with **named return values** to modify or check error states.

---

## **Go Is Call by Value**
Go always **copies** the value of parameters:
```go
type person struct {
    name string
    age  int
}

func modifyFails(i int, s string, p person) {
    i = i * 2        // local change only
    s = "Goodbye"    // local change only
    p.name = "Bob"   // modifies 'p' inside the function
}

func main() {
    p := person{"Alice", 30}
    i := 2
    s := "Hello"

    modifyFails(i, s, p)
    fmt.Println(i, s, p) // 2 Hello {Alice 30}
}
```
- With **maps** and **slices**, the “value” is a **pointer** to underlying data, so changes can propagate outside:
  ```go
  func modMap(m map[int]string) {
      m[2] = "hello"
  }
  ```
  > The map variable is copied, but the underlying storage is shared.

---

## **Summary and Quick Revision**
1. **Function Declarations**: Combine `func` with parameters and optional return types.  
2. **Multiple Returns**: Return errors and results together. Check for `err != nil`.  
3. **Anonymous Functions & Closures**: Dynamically create inlined logic that can capture state.  
4. **defer**: Attach cleanup logic that runs at function exit.  
5. **Call by Value**: Go passes copies of values, but references like maps and slices can share underlying data.

### **Extra Tips**
- Use **variadic functions** for flexible arguments but keep an eye on performance for large inputs.  
- Use **function types** to clarify callback signatures.  
- `defer` is especially handy when dealing with resources like files, network connections, or locks.

### **Best Practices**
- **Return Errors** explicitly as the last return value, handle them promptly.  
- **Avoid** blank returns for clarity: always return explicit values.  
- Keep **closures** small and well-defined; watch out for variable shadowing.

### **Common Pitfalls**
1. **Shadowing named return variables** or overshadowing with `:=`.  
2. **Forgetting `...`** when passing a slice to a variadic function.  
3. Using `defer` in **tight loops** can degrade performance.  
4. Overly large closures capturing big data structures might lead to unexpected memory usage.

### **Interview Questions**
1. **How do you handle multiple return values in Go, and why is the error typically last?**  
   <small>Answer Hint: Emphasize Go’s style of error checking and returning `(result, err)` pairs.</small>  
2. **Describe variadic functions in Go. Why must they be the last parameter?**  
   <small>Answer Hint: It’s converted to a slice. Only one variadic parameter is allowed at the end.</small>  
3. **What are the benefits and drawbacks of `defer` for resource management?**  
   <small>Answer Hint: Ensures cleanup, but can impact performance if called repeatedly inside loops.</small>  
4. **Explain how closures capture variables in Go.**  
   <small>Answer Hint: They bind to the outer scope’s variables, allowing read/write access.</small>  
5. **Why might “blank returns” be discouraged in professional Go code?**  
   <small>Answer Hint: They obscure what’s being returned, making code harder to maintain.</small>  

---

> **Next Steps**: Experiment with writing small programs that leverage multiple returns, closures, and `defer` for resource management. Practice passing functions as parameters to see how first-class functions simplify callback patterns in Go.
