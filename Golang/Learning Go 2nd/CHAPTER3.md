# Composite Types

In this chapter, you'll learn about the ***composite types*** in Go, the built-in functions that support them, and the best practices for working with them.

## Arrays - Too Rigid to Use Directly

All elements in the ***array*** must be of the type that's specified. In the first, you specify the ***size*** of the array and the type of the elements in the array:

```go
var x [3]int
```

If you have **initial values** for the array, you specify them with an array literal:

```go
var x = [3]int{10, 20, 30}
```

If you have a **sparse array** (an array where most elements are set to their zero value), you can specify only the indices with nonzero values in the array literal:

```go
var x = [12]int{1, 5: 4, 6, 10: 100, 15} // [1, 0, 0, 0, 0, 4, 6, 0, 0, 0, 100, 15]
```

When using an ***array literal*** to initialize an array, you can replace the number that specifies the number of elements in the array with ***...***:

```go
var x = [...]int{10, 20, 30}
```

You can use *== and !=* to compare two arrays. Arrays are equal if they are the **same length and contain equal values**: 

```go
var x = [...]int{10, 20, 30}
var y = [3]int{10, 20, 30}
fmt.Println(x == y) // true
```

Go has only one-dimensional arrays, but you can simulate ***multidimensional arrays***:

```go
var x [2][3]int
```

Like most languages, arrays in Go are read and written using ***bracket syntax***:

```go
x[5] = 1
```

You cannot read or write past the *end of an array* or use a *negative index*.

Finally, the built-in function ***len*** takes in an array and returns its length:

```go
var x = [3]int{10, 20, 30}
fmt.Println(len(x)) // 3
```

Go considers the ***size of the array*** to be part of the type of the array. This also means that you **cannot** use a variable to specify the size of an array, because **types must be resolved at compile time**, not at runtime.

What's more, you ***can't*** use a type conversion to directly convert arrays of different sizes to identical types. Because you can't convert arrays of different sizes into each other, you ***can't*** write a function that works with arrays of any size and you ***can't*** assign arrays of different sizes to the same variable.

> *Because of these restrictions, don't use arrays unless you know the* ***exact length*** *you need ahead of time.*

## Slices

What makes slices so useful is that **you can grow slices as needed**. This is because the length of a slice is not part of its type.

The first thing to notice is that you ***don't*** specify the size of the slice when you declare it:

```go
var x []int{10, 20, 30}
```

> *Using [...] makes an array. Using [ ] makes a slice.*

This creates a slice of three ints using a ***slice literal***. Just as with arrays, you can also specify only the ***indices*** with nonzero values in the slice literal:

```go
var x = []int{1, 5: 4, 6, 10: 100, 15} // [1, 0, 0, 0, 0, 4, 6, 0, 0, 0, 100, 15]
```

You can simulate ***multidimensional slices*** and make a slice of slices:

```go
var x [][]int
```

You read and write slices using ***bracket syntax***, and, just as with arrays, you can't read or write past the end or use a negative index:

```go
x[5] = 1
```

You start to see the differences between arrays and slices when you look at declaring slices **without** using a literal:

```go
var x []int
```

Since no value is assigned, x is assigned the zero value for a slice, which is something you haven't seen before: ***nil***. In Go, nil is an identifier that represents the ***lack of a value*** for some types. **A nil slice contains nothing.**

A **slice** is the first type you've seen that **isn't comparable**. The only thing you can compare a slice with using == is ***nil***:

```go
fmt.Println(x == nil) // true
```

Since **Go 1.21**, the slices package in the standard library includes two functions to compare slices. The ***slices.Equal*** function takes in two slices and returns *true* if the slices are the same length, and all of the elements are equal.

The other function, ***slices.EqualFunc***, lets you pass in a function to determine equality and does not require the slice elements to be comparable.

```go
x := []int{1, 2, 3, 4, 5}
y := []int{1, 2, 3, 4, 5}
z := []int{1, 2, 3, 4, 5, 6}
s := []string{"a", "b", "c"}
fmt.Println(slices.Equal(x, y)) // prints true
fmt.Println(slices.Equal(x, z)) // prints false
fmt.Println(slices.Equal(x, s)) // does not compile
```

### len

It works for slices too. Passing a ***nil slice*** to len returns 0.

### append

The built-in append function is used to grow slices:

```go
var x []int
x = append(x, 10)
```

The **append function** takes at least two parameters, a slice of any type and a value of that type. It returns a ***new slice*** with the value appended to the end.

```go
var x = []int{10, 20, 30}
x = append(x, 40)
```

You can append **more than one** value at a time:

```go
var x = []int{10, 20, 30}
x = append(x, 40, 50, 60)
```

One **slice is appended onto another** by using the ***...*** operator to expand the source slice into individual values:

```go
var x = []int{10, 20, 30}
var y = []int{40, 50, 60}
x = append(x, y...)
```

> *It is a compile-time error if you forget to assign the value returned from append.*

### Capacity

Every slice also has a ***capacity***, which is the **number of consecutive memory locations reserved**. If you try to add additional values when the *length equals the capacity*, the append function uses the ***Go runtime*** to allocate a new backing array for the slice with a larger capacity.

>  *The* ***Go runtime*** *provides services like memory allocation and garbage collection, concurrency support, networking, and implementations of built-in types and functions.* ***The Go runtime is compiled into every Go binary.***

When a slice grows via append, it takes time for the Go runtime to **allocate new memory and copy the existing data from the old memory to the new**. The old memory also needs to be ***garbage collected***.

Just as the built-in len function returns the current length of a slice, the built-in ***cap*** function returns the ***current capacity of a slice***.

```go
var x = []int{10, 20, 30}
fmt.Println(len(x)) // 3
fmt.Println(cap(x)) // 3
```

While it's nice that slices grow automatically, **it's far more efficient to size them once**.

### make

It allows you to specify the **type, length, and, optionally, the capacity**.

```go
x := make([]int, 3, 5)
```

*This creates an int slice with a length of 5 and a capacity of 5. Since it has a length of 5, x[0] through x[4] are valid elements, and they are all initialized to 0.*

You can also specify an **initial capacity** with make:

```go
x := make([]int, 3, 5)
```

You can also create a slice with **zero length but a capacity** that's greater than zero:

```go
x := make([]int, 0, 5)
```

In this case, you have a ***non-nil slice*** with a **length of 0** but a **capacity of 10**. Since the length is 0, you **can't directly index into it**, but you can append values to it:

```go
x := make([]int, 0, 10)
x = append(x, 10, 20, 30)
```

> ***Never specify a capacity that's less than the length!***

### Emptying a Slice

**Go 1.21** added a clear function that takes in a slice and **sets all of the slice's elements to their zero value**.

```go
x := []int{10, 20, 30}
fmt.Println(x, len(x), cap(x)) // [10, 20, 30] 3 3
clear(x)
fmt.Println(x, len(x), cap(x)) // [0, 0, 0] 3 3
```

### Declaring Your Slice

*The primary goal is to minimize the number of times the slice needs to grow.*

```go
var x []int // nil slice
var y = []int{} // empty slice
```

Because of implementation reasons, comparing a zero-length slice to *nil* returns false, while comparing a *nil* slice to *nil* returns true.

> *For simplicity,* ***favor nil slices***. *A zero-length slice is useful only when converting a slice to JSON.

If you have a good idea of how large your slice needs to be, but don't know what those values will be when you are writing the program, use ***make***.

### Slicing Slices

A ***slice expression*** creates a slice from a slice. It's written inside brackets and consists of a starting offset and an ending offset, separated by a ***colon ( : )***. If you leave off the starting offset, 0 is assumed. Likewise, if you leave off the ending offset, the end of the slice is substituted.

```go
x := []string{"z", "y", "x", "w"}
y := x[:2]
z := x[1:]
d := x[1:3]
e := x[:]
fmt.Println("x:", x) // [z y x w]
fmt.Println("y:", y) // [z y]
fmt.Println("z:", z) // [y x w]
fmt.Println("d:", d) // [y x]
fmt.Println("e:", e) // [z y x w]
```

*When you take a slice from a slice, you are not making a copy of the data.* Instead, you now have two variables that are ***sharing memory***.

```go
x := []string{"a", "b", "c", "d"}
y := x[:2]
z := x[1:]
x[1] = "y"
y[0] = "x"
z[1] = "z"
fmt.Println("x:", x) // [x y z d]
fmt.Println("y:", y) // [x y]
fmt.Println("z:", z) // [x y z]
```

Slicing slices gets extra **confusing** when combined with *append*.

```go
x := []string{"a", "b", "c", "d"}
y := x[:2]
fmt.Println(cap(x), cap(y)) // 4 4
y = append(y, "z")
fmt.Println("x:", x) // [a b z d]
fmt.Println("y:", y) // [a b z]
```

> *This means elements of the original slice beyond the end of the subslice, including unused capacity, are* ***shared by both slices***.

To avoid complicated slice situations, the ***full slice expression*** includes a third part, which indicates the **last position in the parent slice's capacity** that's available for the subslice.

```go
x := make([]string, 0, 5)
x = append(x, "a", "b", "c", "d")
y := x[:2:2]
z := x[2:4:4]
```

> *Use a three-part slice expression to prevent append from sharing capacity between slices.*

#### copy

If you need to create a slice that's ***independent*** of the original, use the built-in *copy* function.

```go
x := []int{1, 2, 3, 4}
y := make([]int, 4)
num := copy(y, x)
fmt.Println(y, num) // [1 2 3 4] 4
```

The function copies ***as many values as it can*** from source to destination, **limited by whichever slice is smaller**, and ***returns*** the number of elements copied.

You can also *copy* a ***subset*** of a slice.

```go
x := []int{1, 2, 3, 4}
y := make([]int, 2)
num := copy(y, x) // [1 2] 2
```

You could also *copy* from the ***middle*** of the source slice.

```go
x := []int{1, 2, 3, 4}
y := make([]int, 2)
copy(y, x[2:]) // [3 4] 2
```

> *If you don't need the number of elements copied, you don't need to assign it*.

The copy function allows you to copy between two slices that cover ***overlapping sections*** of an underlying slice:

```go
x := []int{1, 2, 3, 4}
num := copy(x[:3], x[1:])
fmt.Println(x, num) // [2 3 4 4] 3
```

You can use *copy* with arrays by taking a slice of the array.

```go
x := []int{1, 2, 3, 4}
d := [4]int{5, 6, 7, 8}
y := make([]int, 2)
copy(y, d[:])
fmt.Println(y) // [5 6]
copy(d[:], x)
fmt.Println(d) // [1 2 3 4]
```

### Converting Arrays to Slices

You can convert an ***array to a slice*** by taking a slice of the array.

```go
x := [4]int{1, 2, 3, 4}
y := x[:3] // subset of x
```

> ***Be aware that taking a slice from an array has the same memory-sharing properties as taking a slice from a slice.***

### Converting Slices to Arrays

You can convert an entire ***slice to an array*** of the same type, or you can create an array from a subset of the slice.

When you convert a slice to an array, ***the data in the slice is copied to new memory***. That means that changes to the slice won't affect the array, and vice versa.

```go
xSlice := []int{1, 2, 3, 4}
xArray := [4]int(xSlice)
smallArray := [2]int(xSlice)
xSlice[0] = 10
fmt.Println(xSlice) // [10 2 3 4]
fmt.Println(xArray) // [1 2 3 4]
fmt.Println(smallArray) // [1 2]
```

> *It's a compile-time error to use [...] in a slice to array type conversion.*

> ***While the size of the array can be smaller than the size of the slice, it cannot be bigger.***

```go
panicArray := [5]int(xSlice)
fmt.Println(panicArray) // [1 2 3 4 0]
```

## Strings and Runes and Bytes

Under the covers, Go uses a ***sequence of bytes*** to represent a string.

> *According to the language specification, Go source code is always written in UTF-8.*

Just as you can extract a single value from an array or a slice, you can extract a single value from a *string* by using an ***index expression***:

```go
x := "hello"
fmt.Println(x[1]) // 101 (ASCII value of 'e')
```

The ***slice expression*** notation that you used with arrays and slices also works with *strings*:

```go
x := "hello"
fmt.Println(x[1:4]) // ell
```

Since ***strings are immutable***, they don't have the modification problems that slices of slices do. But when dealing with languages other than English or with emojis, you run into ***code points*** that are **multiple bytes long** in UTF-8:

```go
x := "hello, 世界"
fmt.Println(x[7]) // 228
```

Go allows you to pass a string to the built-in len function to find the **length of the string**.

```go
x := "hello, 世界"
fmt.Println(len(x)) // 13
```

> *Even though Go allows you to use slicing and indexing syntax with strings, you should use it only when you know that your string contains only characters that take up one byte.*

Because of this ***complicated relationship*** among runes, strings, and bytes, Go has some interesting ***type conversions*** between these types.

```go
var a rune = 'x' // 120
var s1 string = string(a) // "x"
var b byte = 'y' // 121
var s2 string = string(b) // "y"
```

> *As of Go 1.15, go vet blocks a type conversion to string from any integer type other than rune or byte.*

A string can be converted back and forth to a slice of bytes or a slice of runes.

```go
x := "hello 🤣"
y := []byte(x)
z := []rune(x)
fmt.Println(y) // [104 101 108 108 111 32 240 159 164 163]
fmt.Println(z) // [104 101 108 108 111 32 129315]
```

The first output line has the string converted to ***UTF-8 bytes***. The second has the string converted to ***runes***.

Most data in Go is read and written as a ***sequence of bytes***, so the most common string type conversions are back and forth with a ***slice of bytes***. Slices of runes are uncommon.

> *Fun fact: UTF-8 was invented in 1992 by Ken Thompson and Rob Pike, two of the creators of Go.*

## Maps

Like most languages, Go provides a built-in data type for situations where you want to ***associate one value to another***. First, you can use a var declaration to create a map variable that's set to its ***zero value***:

```go
var nilMap map[string]int // nil map
```

Attempting to read a nil map ***always returns the zero value*** for the map's value type. However, attempting to write to a nil map variable ***causes a panic***.

You can use a ***:= declaration*** to create a map variable by assigning it a map literal:

```go
x := map[string]int{"one": 1, "two": 2} // literal, non empty
y := map[string]int{} // empty map, not nil
```

If you know how many key-value pairs you intend to put in the map but don't know the exact values, you can use ***make*** to create a map with a default size:

```go
ages := make(map[int][]string, 10) // 0 length, 10 capacity and beyond
```

***Maps*** are like ***slices*** in several ways:
- ***Automatically grow*** as you add key-value pairs to them.
- You can use make to create a map with a ***specific initial size***.
- *len* function tells you the ***number of key-value pairs*** in a map.
- The ***zero value*** for a map is ***nil***.
- You can check if they are ***equal to nil***, but you ***cannot check*** if two maps have identical keys and values using *== or differ using !=*.

> ***The key for a map can be any comparable type.***

> *The map that's built into Go is a hash map, or hash table. It's great that Go includes a hash map implementation as part of the runtime, because building your own is hard to get right.*

### Reading and Writing a Map

Let's look at a short program that declares, writes to, and reads from a map.

```go
x := map[string]int{}
x["one"] = 1
fmt.Println(x["one"]) // 1
x["three"] = 3
fmt.Println(x["three"]) // 3
x["three"]++ // add 1 to the value
fmt.Println(x["three"]) // 4
fmt.Println(x["two"]) // 0
```

When you try to read the value assigned to a map key that was never set, ***the map returns the zero value*** for the map's value type.

> *You can use the ++ operator to increment the numeric value for a map key.*

### The comma ok idiom

Go provides the ***comma ok idiom*** to tell the difference between a key that's associated with a ***zero value*** and a key that's ***not in the map***:

```go
m := map[string]int{ 
    "hello": 5, 
    "world": 0,
}
v, ok := m["hello"]
fmt.Println(v, ok) // 5 true
v, ok = m["world"]
fmt.Println(v, ok) // 0 true
v, ok = m["goodbye"]
fmt.Println(v, ok) // 0 false
```

> *The comma ok idiom is used in Go when you want to differentiate between reading a value and getting back the zero value.*

### Deleting from Maps

Key-value pairs are removed from a map via the built-in delete function:

```go
m := map[string]int{
    "hello": 5,
    "world": 0,
}
delete(m, "world") // map[hello:5]
```

> *The delete function doesn't return a value.*

### Emptying a Map

A ***cleared map has its length set to zero***, unlike a cleared slice.

```go
clear(m)
fmt.Println(m) // map[]
```

### Comparing Maps

***Go 1.21*** added a package to the standard library called maps that contains ***helper functions*** for working with maps. Two functions in the package are useful for comparing if two maps are equal, ***maps.Equal and maps.EqualFunc***.

```go
n := map[string]int{
    "hello": 5,
    "world": 0,
}
o := map[string]int{
    "hello": 5,
    "world": 0,
}
fmt.Println(maps.Equal(n, o)) // true
```

### Using Maps as Sets

A ***set*** is a data type that ensures there is ***at most one*** of a value, but doesn't guarantee that the values are in any particular order.

> ***Go doesn't include a set, but you can use a map to simulate some of its features.***

Use the key of the map for the type that you want to put into the set and use a bool for the value.

```go
intSet := map[int]bool{}
vals := []int{5, 10, 2, 5, 8, 7, 3, 9, 1, 2, 10}
for _, v := range vals {
    intSet[v] = true
}
fmt.Println(len(vals), len(intSet)) // 11 9
fmt.Println(intSet[5]) // true
fmt.Println(intSet[500]) // false
```

> *You want a set of ints, so you create a map where the keys are of int type and the values are of bool type.*

Some people prefer to use struct{} for the value when a map is being used to implement a set.

```go
intSet := map[int]struct{}{}
vals := []int{5, 10, 2, 5, 8, 7, 3, 9, 1, 2, 10}
for _, v := range vals {
    intSet[v] = struct{}{}
}
if _, ok := intSet[5]; ok {
    fmt.Println("5 is in the set")
}
```

The advantage is that an ***empty struct uses zero bytes***, while a boolean uses one byte.

## Structs

When you have ***related data*** that you want to group together, you should define a struct.

> ***Go doesn't have classes, because it doesn't have inheritance.***

```go
type person struct {
    name string
    age int
}
```

Also note that unlike in map literals, ***no commas separate*** the fields in a struct declaration. You can define a struct type ***inside or outside*** of a function.

Once a struct type is declared, you can define variables of that type. A ***zero value struct*** has every field set to the field's zero value.:

```go
var sub1 person
sub1.name = "Bob" // Accessed using the dot operator
sub1.age = 20 // Accessed using the dot operator
var sub2 person
fmt.Println(sub1) // {Bob 20}
fmt.Println(sub2) // { 0} (empty string and 0, zero values)
```

Unlike maps, there is ***no difference*** between assigning an empty struct literal and not assigning a value at all. Both initialize all fields in the struct to their zero values.

When using this ***struct literal format***, a value for every field in the struct must be specified, and the values are assigned to the fields ***in the order*** they were declared in the ***struct definition***.

You use the ***names of the fields*** in the struct to specify the values. It allows you to specify the fields in ***any order***, and you ***don't need*** to provide a value for all fields

A ***struct literal*** can be assigned to a variable as well:

```go
sub3 := person{}
sub4 := person{"Alice", 30}
sub5 := person{name: "Charlie", age: 40}
sub6 := person{age: 50, name: "David"}
```

> ***You cannot mix the two struct literal styles: either all fields are specified with names, or none of them are***

### Anonymous Structs

You can also declare that a variable implements a struct type ***without first giving the struct type a name***.

```go
var person struct {
    name string
    age int
}
person.name = "Alice"
person.age = 30
```

Useful when you translate external data into a struct or a struct into external data (***like JSON or Protocol Buffers***). This is called ***unmarshaling and marshaling*** data, respectively.

### Comparing and Converting Structs

Structs that are entirely composed of ***comparable types*** are comparable; those with slice or map fields are not.

Go ***doesn't allow*** comparisons between variables that represent structs of different types. Go does allow you to perform a ***type conversion*** from one struct type to another if the fields of both structs have the ***same names, order, and types***.

```go
// firstPerson can only compare with another firstPerson
type firstPerson struct {
    name string
    age int
}
// firstPerson can be converted to secondPerson, same field order, names, and types
type secondPerson struct { 
    name string
    age int
}
// firstPerson can't be converted to thirdPerson, different field order
type thirdPerson struct {
    age int
    name string
}
// firstPerson can't be converted to fourthPerson, different field names
type fourthPerson struct {
    firstName string
    age int
}
// firstPerson can't be converted to fifthPerson, different field count
type fifthPerson struct {
    name string
    age int
    city string
}
```

***Anonymous structs*** add a small twist: if two struct variables are being compared and at least one has a type that's an anonymous struct, you can compare them without a ***type conversion*** if the fields of both structs have the ***same names, order, and types***. 

You can also ***assign*** between named and anonymous struct types if the fields of both structs have the ***same names, order, and types***:

```go
// firstPerson struct type
type firstPerson struct { 
    name string age int
}
f := firstPerson{
    name: "Bob", age: 50,
}
// Anonymous struct type
var g struct {
    name string age int
}
// compiles -- can use = and == between identical named and anonymous structs
g = f // assignment
fmt.Println(f == g) // true
```