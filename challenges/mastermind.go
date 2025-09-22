package challenges // Belongs to the 'challenges' package because it's in the 'challenges' directory

import (
    "encoding/json"
    "net/http"
	"fmt"
	"math/rand"
)

func MastermindHandler(w http.ResponseWriter, r *http.Request) {
    // For now, let's just return a simple message.
    response := map[string]string{"challenge": "Mastermind"}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
	var secretCode [4]string 

	var guess [4]string
	fmt.Scanln(&guess)

}

