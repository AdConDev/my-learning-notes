# Exponential Backoff in Go

Exponential backoff retries failed operations with increasing delays (e.g., 1s, 2s, 4s) to avoid overwhelming systems. Add jitter (random variation) to prevent synchronized retries.

## Key Concept

- **Base delay**: Initial wait time.
- **Multiplier**: Doubles delay each retry.
- **Max retries**: Limit attempts.
- **Jitter**: Randomize delay to spread load.

## Simple Example

```go
package main

import (
	"fmt"
	"math/rand"
	"time"
)

func retryWithBackoff(operation func() error, maxRetries int) error {
	baseDelay := time.Second // Initial delay
	for attempt := 0; attempt < maxRetries; attempt++ {
		err := operation() // Execute operation
		if err == nil {
			return nil // Success
		}
		fmt.Printf("Attempt %d failed: %v\n", attempt+1, err)

		if attempt < maxRetries-1 { // Not last attempt
			delay := baseDelay * time.Duration(1<<attempt) // Exponential: 1s, 2s, 4s...
			jitter := time.Duration(rand.Intn(1000)) * time.Millisecond // Random 0-1s
			time.Sleep(delay + jitter) // Wait with jitter
		}
	}
	return fmt.Errorf("max retries exceeded")
}

func main() {
	rand.Seed(time.Now().UnixNano())
	operation := func() error {
		// Simulate failure 80% of time
		if rand.Float32() < 0.8 {
			return fmt.Errorf("temporary error")
		}
		return nil
	}
	err := retryWithBackoff(operation, 5)
	if err != nil {
		fmt.Println("Final error:", err)
	} else {
		fmt.Println("Success!")
	}
}
```

## Explanation

- **Exponential growth**: `1<<attempt` doubles delay (bit shift for efficiency).
- **Jitter**: Adds randomness to avoid thundering herd (all retries at once).
- **Loop**: Retries up to maxRetries; sleeps between attempts.
- **Use case**: HTTP requests, DB connections; combine with context for cancellation.