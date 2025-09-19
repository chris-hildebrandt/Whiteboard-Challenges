package main

import (
	"fmt"
	"log"
	"net/http"
)

// apiHandler will be a placeholder for future API logic.
func apiHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello from the Go API!")
}

func main() {
	http.HandleFunc("/api", apiHandler)
	fmt.Println("Starting server on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
