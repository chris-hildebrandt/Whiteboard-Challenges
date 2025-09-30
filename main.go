package main

import (
	"fmt"
	"log"
	"net/http"
	"whiteboard-challenges/challenges"
)

// apiHandler will be a placeholder for future API logic.
func apiHandler(w http.ResponseWriter, r *http.Request) {
	// Let's make this a proper JSON response for consistency.
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"message": "Hello from the Go API!"}`))
}

func main() {
	fmt.Println(consoleGreet())
	http.HandleFunc("/api", apiHandler)
	http.HandleFunc("/mastermind", challenges.MastermindHandler)
	http.HandleFunc("/letterCounter", challenges.LetterCounterHandler)
	fmt.Println("Starting server on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
