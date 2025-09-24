package challenges // Belongs to the 'challenges' package because it's in the 'challenges' directory

import (
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
)

// Future goal: state management solution like a session or a database, to handle multiple players.
var secretCode [4]string
var colors = []string{"red", "yellow", "blue", "green", "orange", "purple"}

// MastermindHandler starts a new game. On a GET request, it generates a new
// secret code and returns the list of available colors.
func MastermindHandler(w http.ResponseWriter, r *http.Request) {

	// Generate a new secret code for the game.
	for i := 0; i < 4; i++ {
		secretCode[i] = colors[rand.Intn(len(colors))]
	}

	// For debugging purposes, let's print the secret code to the server console.
	fmt.Println("New game started. Secret code:", secretCode)

	// The response to the frontend includes the available colors for the UI.
	response := map[string]interface{}{
		"challenge": "Mastermind",
		"colors":    colors,
		"message":   "New game started. Make a guess!",
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// MastermindGuessRequest defines the structure for a guess from the frontend.
type MastermindGuessRequest struct {
	Guess []string `json:"guess"`
}

// MastermindGuessHandler handles a user's guess. It expects a POST request
// with a JSON body containing the guess.
func MastermindGuessHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	// Read and decode the JSON body from the request.
	var requestData MastermindGuessRequest
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()
	json.Unmarshal(body, &requestData)

	guess := requestData.Guess
	fmt.Println("Received guess:", guess)

	// --- Mastermind Scoring Logic ---
	correctColorAndPosition := 0
	correctColor := 0

	secretUsed := [4]bool{}
	guessUsed := [4]bool{}

	for i := 0; i < 4; i++ {
		if guess[i] == secretCode[i] {
			correctColorAndPosition++
			secretUsed[i] = true
			guessUsed[i] = true
		}
	}

	for i := 0; i < 4; i++ {
		if guessUsed[i] {
			continue
		}
		for j := 0; j < 4; j++ {
			if !secretUsed[j] && guess[i] == secretCode[j] {
				correctColor++
				secretUsed[j] = true
				break
			}
		}
	}

	// Prepare and send the response to the frontend.
	response := map[string]interface{}{
		"hits":  correctColorAndPosition,
		"blows": correctColor,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}
