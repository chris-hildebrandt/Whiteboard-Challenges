package challenges

import (
	"encoding/json"
	"io"
	"net/http"
	"strings"
)

// Define a struct to decode the incoming JSON request
type LetterCounterRequest struct {
	Input string `json:"input"`
}

func LetterCounterHandler(w http.ResponseWriter, r *http.Request) {
	// Decode the incoming JSON request from the frontend
	var requestData LetterCounterRequest
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()
	json.Unmarshal(body, &requestData)

	input := requestData.Input
	alphabet := "abcdefghijklmnopqrstuvwxyz"
	
	counts := make(map[string]int)

	for i := 0; i < len(alphabet); i++ {
		count := 0
		for j := 0; j < len(input); j++ {
			if strings.EqualFold(string(alphabet[i]), string(input[j])) {
				count++
			}
		}
		if count > 0 {
			counts[string(alphabet[i])] = count
		}
	}

	// Prepare the response.
	response := map[string]interface{}{
		"input":  input,
		"counts": counts,
	}

	// Send the response as JSON.
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}
