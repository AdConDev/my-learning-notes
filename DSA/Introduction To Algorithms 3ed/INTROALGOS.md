# Introduction To Algorithms 4th Edition

## Chapter 1: The Role of Algorithms in Computing

### Algorithms

An algorithm is thus a sequence of computational steps that transform the input into the output. An algorithm for a computational problem is correct if, for every problem instance provided as input, it halts - finishes its computing in finite time - and outputs the correct solution to the problem instance.

A data structure is a way to store and organize data in order to facilitate access and modifications.

## Chapter 2: Getting Started

### Loop Invariants

Loop invariants help us understand why an algorithm is correct. When you’re using a loop invariant, you need to show three things:

Initialization: It is true prior to the first iteration of the loop.

Maintenance: If it is true before an iteration of the loop, it remains true before the next iteration.

Termination: The loop terminates, and when it terminates, the invariant usually along with the reason that the loop terminated gives us a useful property that helps show that the algorithm is correct.

### The Divide-and-Conquer Method

In the divide-and-conquer method, if the problem is small enough - the base case - you just solve it directly without recursing. Otherwise - the recursive case - you perform three characteristic steps:

Divide the problem into one or more subproblems that are smaller instances of the same problem.

Conquer the subproblems by solving them recursively.

Combine the subproblem solutions to form a solution to the original problem.
