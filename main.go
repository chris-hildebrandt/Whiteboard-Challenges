package main

import (
	"fmt"
	"log"
	"net/http"
	"whiteboard-challenges/challenges"
)

func apiHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"message": "Hello from the Go API!"}`))
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/api", apiHandler)
	mux.HandleFunc("/mastermind", challenges.MastermindHandler)
	mux.HandleFunc("/letterCounter", challenges.LetterCounterHandler)
	mux.HandleFunc("/workingHoursCalculator", challenges.WorkingHoursCalculatorHandler)

	fmt.Println("Starting server on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", mux))
}
