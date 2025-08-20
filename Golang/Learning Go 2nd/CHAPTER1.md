# Setting Up Your Go Environment

Every programming language needs a ***development environment***, and Go is no exception.

## Installing the Go Tools

To build Go code, you need to download and install the ***Go development tools***.

> *Go programs compile to a single native binary and do not require any additional software to be installed in order to run them. Using a single native binary makes it a lot easier to distribute programs written in Go.*

## Go Tooling

All of the Go development tools are accessed via the ***go command***. In addition to go version, there's a compiler (***go build***), code formatter (***go fmt***), dependency manager (***go mod***), test runner (***go test***), a tool that scans for common coding mistakes (***go vet***), and more.

## Making a Go Module

***A Go project is called a module.*** A module is not just source code. It is also an ***exact specification*** of the dependencies of the code within the module.

You ***shouldn't*** edit the go.mod file directly. Instead, use the go get and ***go mod tidy*** commands to manage changes to the file.

> *What is a language server? It's a standard specification for an API that enables editors to implement intelligent editing behavior, like code completion, quality checks, or finding all the places a variable or function is used in your code.*

## Staying Up-to-Date

Go programs compile to a standalone native binary, so you ***don't need to worry*** that updating your development environment could cause your currently deployed programs to fail.