package main

import (
	"encoding/json"
	"fmt"
	"log"
	"math"
)

func LinearSearch(arr []int, target int) int {
	for i, v := range arr {
		if target == v {
			return i
		}
	}
	return -1
}

func BubbleSort(arr []int) {
	n := len(arr)              // Get array length
	for i := 0; i < n-1; i++ { // Outer loop
		swap := false                // Track if elements were swapped
		for j := 0; j < n-i-1; j++ { // Compare adjacent elements
			if arr[j] > arr[j+1] { // Swap if out of order
				arr[j], arr[j+1] = arr[j+1], arr[j]
				swap = true
			}
		}
		if !swap { // No swaps means already sorted
			break
		}
	}
}

func chapter2() {
	const x = 20
	var i int = x
	var f float64 = x
	fmt.Println(i, f)
	var b byte = math.MaxUint8
	var smallI int32 = math.MaxInt32
	var bigI uint64 = math.MaxUint64
	b += 1
	smallI += 1
	bigI += 1
	fmt.Println(b, smallI, bigI)
	arr := []int{64, 34, 25, 12, 22, 11, 90}
	BubbleSort(arr)
	fmt.Println("Sorted array:", arr)
	fmt.Println(LinearSearch(arr, 90))
}

type Kid struct {
	Age     int `json:"age"`
	Candies int `json:"candies"`
}

func main() {
	// Raw JSON string
	rawJson := "[{\"age\": 5, \"candies\": 20},{\"age\": 6, \"candies\": 15}]"

	// Create a slice to hold the unmarshaled data
	var kids []Kid

	// Unmarshal the JSON string into the slice
	err := json.Unmarshal([]byte(rawJson), &kids)
	if err != nil {
		log.Fatalf("Error unmarshaling JSON: %v", err)
	}

	// Print the result
	fmt.Printf("%+v\n", kids)
}
