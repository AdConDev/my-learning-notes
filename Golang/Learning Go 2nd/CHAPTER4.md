# Blocks, Shadows, and Control Structures

Now that I have covered variables, constants, and built-in types, you are ready to look at programming logic and organization.

## Blocks

Each place where a declaration occurs is called a ***block***. Variables, constants, types, and functions declared outside of any functions are placed in the ***package block***. All the variables defined at the top level of a function (including the parameters to a function) are in a block.

You can access an identifier defined in any outer block from within any inner block.

## Shadowing Variables

A shadowing variable is a variable that has the same name as a variable in a containing block.

I mentioned in the previous chapter that in some situations I avoid using ***:=*** because it can make it ***unclear what variables are being used***.

```go
func main() {
    x := 10
    if x > 5 {
        x, y := 5, 10
        fmt.Println(x) // 5
    }
    fmt.Println(x) // 10
}
```

> *When using :=, make sure that you don't have any variables from an outer scope on the lefthand side unless you intend to shadow them.*

### The Universe Block

The ***universe block*** is the block that contains all the built-in types, functions, and constants. It is ***the outermost block***.

Rather than make them ***keywords***, Go considers these ***predeclared identifiers*** and defines them in the universe block, which is ***the block that contains all other blocks***.

## if Statements

The ***if statement*** in Go is much like the if statement in most programming languages.

```go
if x > 5 {
    fmt.Println("x is greater than 5")
} else {
    fmt.Println("x is less than or equal to 5")
}
```

The most visible difference between if statements in Go and other languages is that you ***don't put parentheses around the condition***.

What Go adds is the ability to ***declare variables*** that are scoped to the condition and to both the if and else blocks. It lets you create variables that are available ***only where they are needed***.

```go
if x := 5; x > 5 {
    fmt.Println("x is greater than 5")
} else {
    fmt.Println("x is less than or equal to 5")
}
```

> *Use this feature only to define new variables that are scoped to the if/else statements; anything else would be confusing.*

## for in Four Ways

What makes Go different from other languages is that ***for is the only looping keyword*** in the language.

- A complete, ***C-style for***
- A ***condition-only for***
- An ***infinite for***
- ***for-range***

### The Complete for Statement

The first for loop style is the complete for declaration.

```go
for i := 0; i < 10; i++ {
    fmt.Println(i)
}
```

Just like the ***if statement***, the ***for statement*** does not use parentheses around its parts. First, you must ***use := to initialize the variables; var is not legal here***. Second, just as variable declarations in ***if statements***, you can ***shadow*** a variable here.

The second part is the ***comparison***. This must be an expression that evaluates to a ***bool***.

The last part of a standard for statement is the ***increment***.

Most commonly, you'll either ***leave off the initialization*** if it is based on a value calculated before the loop:

```go
i := 0
for ; i < 10; i++ { fmt.Println(i)
}
```

or you'll ***leave off the increment*** because you have a more complicated increment rule inside the loop:

```go
for i := 0; i < 10; {
    fmt.Println(i)
    if i % 2 == 0 {
        i++
    } else {
        i+=2
    }
}
```

### The Condition-Only for Statement

When you ***leave off both the initialization and the increment*** in a ***for statement***, do not include the semicolons

```go
i := 1
for i < 100 {
    fmt.Println(i)
    i = i * 2
}
```

### The Infinite for Statement

Go has a version of a for loop that loops forever.

```go
func main() { for {
    fmt.Println("Hello") }
}
```

> *Press Ctrl-C when you are tired of walking down memory lane.*

### break and continue

It ***exits the loop*** immediately, just like the ***break statement*** in other languages.

> *If you want to iterate at least once, the cleanest way is to use an infinite for loop that ends with an if statement.*

Go also includes the ***continue keyword***, which skips over the rest of the for loop's body and ***proceeds directly to the next iteration***.

```go
for i := 1; i <= 100; i++ {
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

Go encourages ***short if statement*** bodies, as left-aligned as possible. Using a ***continue statement*** makes it easier to understand what's going on.

### The for-range Statement

The fourth ***for statement*** format is for iterating over elements in some of Go's built-in types.

First, let's take a look at using a ***for-range loop*** with a ***slice***.

```go
numbers := []int{1, 2, 3, 4, 5}
for i, n := range numbers {
    fmt.Println(i, n)
}
```

The ***first variable is the position*** in the data structure being iterated, while the ***second is the value at that position***.

> *Anytime you are in a situation where a value is returned, but you want to ignore it, use an underscore to hide the value.*

#### Iterating over maps

First, they modified the ***hash algorithm*** for ***maps*** to include a ***random number*** that's generated every time a map variable is created. Next, they made the order of a ***for-range iteration*** over a map ***vary a bit*** each time the map is looped over. These two changes make it far ***harder*** to implement a ***Hash DoS attack***.

> *To make it easier to debug and log maps, the formatting functions (like fmt.Println) always output maps with their keys in ascending sorted order.*

#### Iterating over strings

As I mentioned earlier, you can also use a string with a ***for-range loop***.

```go
for i, r := range "Hello, 世界" {
    fmt.Printf(i, r, string(r)) // index rune(int32) string
}
```

> *The first variable holds the number of bytes from the beginning of the string, but the type of the second variable is rune.*

Whenever a ***for-range loop*** encounters a ***multibyte rune*** in a string, it converts the ***UTF-8*** representation into a ***single 32-bit*** number and assigns it to the value. If the ***for-range loop*** encounters a ***byte*** that doesn't represent a valid ***UTF-8*** value, the ***Unicode replacement character*** (hex value **0xfffd**) is returned instead.

#### The for-range value is a copy

Modifying the ***value variable*** will not modify the value in the ***compound type***.

```go
evenVals := []int{2, 4, 6, 8, 10, 12}
for _, v := range evenVals {
    v *= 2
}
fmt.Println(evenVals) // [2 4 6 8 10 12]
```

Since ***Go 1.22***, the default behavior is to ***create a new index and value variable*** on each iteration through the ***for loop***.

### Labeling Your for Statements

What if you have ***nested for loops*** and want to exit or skip over an iterator of an ***outer loop***?

```go
func main() {
    samples := []string{"hello", "apple_π!"}
outer:
    for _, sample := range samples {
        for i, r := range sample {
            fmt.Println(i, r, string(r)) // 'hel' and 'appl'
            if r == 'l' {
                continue outer
            } 
        }
    fmt.Println()
    }
}
```

Labels are always ***indented to the same level*** as the braces for the block.

### Choosing the Right for Statement

Most of the time, you're going to use the ***for-range format***.

While you could use some combination of ***if, continue, and break*** within a ***for-range loop***, a ***standard for loop*** is a clearer way to indicate the ***start and end*** of your iteration.

The ***condition-only for loop*** is, like the ***while loop*** it replaces, useful when you are looping based on a ***calculated value***.

As shown previously, an ***infinite for loop*** can be combined with an ***if statement*** to simulate the ***do statement*** that's present in other languages.

## switch

Like many ***C-derived languages***, ***Go*** has a switch statement.

```go
words := []string{"a", "cow", "smile", "gopher", "octopus", "anthropologist"}
for _, word := range words {
    switch size := len(word); size {
        case 1, 2, 3, 4:
        fmt.Println(word, "is a short word!")
        case 5:
            wordLen := len(word)
            fmt.Println(word, "is exactly the right length:", wordLen)
        case 6, 7, 8, 9:
        default:
        fmt.Println(word, "is a long word!")
    }
}
```

You can have multiple lines inside a case (or default) clause, and they are ***all considered to be part of the same block***. In Go, an ***empty case*** means ***nothing happens***.

> *For the sake of completeness, Go does include a fallthrough keyword, which lets one case continue on to the next one.*

You can ***switch*** on any type that can be ***compared with ==***, which includes ***all built-in*** types ***except*** slices, maps, channels, functions, and structs that contain fields of these types.

Even though you don't need to put a ***break statement*** at the end of each case clause, you can use them when you want to ***exit early*** from a case.

If you have a ***switch statement inside a for loop***, and you want to ***break out of the for loop***, put a ***label*** on the ***for statement*** and put the name of the ***label*** on the ***break***.

```go
func main() {
loop:
    for i := 0; i < 10; i++ {
        switch i {
        case 0, 2, 4, 6:
            fmt.Println(i, "is even")
        case 3:
            fmt.Println(i, "is divisible by 3 but not 2")
        case 7:
            fmt.Println("exit the loop!")
            break loop
        default:
            fmt.Println(i, "is boring")
        }
    }
}
```

### Blank Switches

A ***regular switch*** only allows you to check a value for ***equality***. A ***blank switch*** allows you to use ***any boolean comparison*** for each case.

```go
words := []string{"hi", "salutations", "hello"}
for _, word := range words {
    switch wordLen := len(word); {
    case wordLen < 5:
        fmt.Println(word, "is a short word!")
    case wordLen > 10:
        fmt.Println(word, "is a long word!")
    default:
        fmt.Println(word, "is exactly the right length.")
    }
}
```

Just as with a ***regular switch statement***, you can optionally include a ***short variable declaration*** as part of your ***blank switch***.

> *Favor blank switch statements over if/else chains when you have multiple related cases. Using a switch makes the comparisons more visible and reinforces that they are a related set of concerns.*

## goto -- Yes, goto

In Go, a ***goto statement*** specifies a ***labeled line of code***, and execution ***jumps*** to it. Go ***forbids*** jumps that ***skip over variable declarations*** and jumps that ***go into an inner or parallel block***.

```go
func main() {
    a := 10
    goto skip // forbidden
    b := 20 // skips declaration
skip:
    c := 30
    fmt.Println(a, b, c)
    if c > a {
        goto inner //forbidden
    }
    if a < b {
    inner: // jump into parallel block
        fmt.Println("a is less than b")
    }
}
```

An use of correct goto:

```go
func main() {
    a := rand.Intn(10)
    for a < 100 {
        if a%5 == 0 {
            goto done
        }
        a = a*2 + 1
    }
    fmt.Println("do something when the loop completes normally")
done:
    fmt.Println("do complicated stuff no matter why we left the loop")
    fmt.Println(a)
}
```

> *You should try very hard to avoid using goto. But in the rare situations where it makes your code more readable, it is an option.*