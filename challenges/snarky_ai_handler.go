package challenges

import (
	"encoding/json"
	"net/http"
	"os/exec"
)

type SnarkyAIRequest struct {
	Input string `json:"input"`
}

func SnarkyAIPromptHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
		return
	}

	cmd := exec.Command("python3", "-c", "from SnarkyAI import SnarkyAI; print(SnarkyAI().get_opening_prompt())", "-u")
	cmd.Dir = "challenges"
	out, err := cmd.CombinedOutput()
	if err != nil {
		http.Error(w, string(out), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"prompt": string(out)})
}

func SnarkyAIHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	var req SnarkyAIRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	cmd := exec.Command("python3", "-c", "from SnarkyAI import SnarkyAI; print(SnarkyAI().get_response(\""+req.Input+"\"))", "-u")
	cmd.Dir = "challenges"
	out, err := cmd.CombinedOutput()
	if err != nil {
		http.Error(w, string(out), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"response": string(out)})
}
