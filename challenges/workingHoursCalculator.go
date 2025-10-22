package challenges

import (
	"encoding/json"
	"io"
	"net/http"
	"time"
)

// WorkingHoursRequest defines the structure for calculating working hours
type WorkingHoursRequest struct {
	StartTime        string  `json:"startTime"`
	EndTime          string  `json:"endTime"`
	WorkStartHour    int     `json:"workStartHour"`    // Default: 9
	WorkEndHour      int     `json:"workEndHour"`      // Default: 17 (5 PM)
	LunchStartHour   int     `json:"lunchStartHour"`   // Default: 12
	LunchEndHour     int     `json:"lunchEndHour"`     // Default: 13 (1 PM)
	DeductLunch      bool    `json:"deductLunch"`      // Default: false
}

// WorkingHoursResponse defines the response structure
type WorkingHoursResponse struct {
	StartTime     string  `json:"startTime"`
	EndTime       string  `json:"endTime"`
	WorkingHours  float64 `json:"workingHours"`
	TotalDays     int     `json:"totalDays"`
	WorkingDays   int     `json:"workingDays"`
	LunchDeducted float64 `json:"lunchDeducted"`
}

// WorkingHoursCalculatorHandler handles requests to calculate working hours
func WorkingHoursCalculatorHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	var requestData WorkingHoursRequest
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	if err := json.Unmarshal(body, &requestData); err != nil {
		http.Error(w, "Invalid JSON format", http.StatusBadRequest)
		return
	}

	// Set defaults if not provided
	if requestData.WorkStartHour == 0 {
		requestData.WorkStartHour = 9
	}
	if requestData.WorkEndHour == 0 {
		requestData.WorkEndHour = 17
	}
	if requestData.LunchStartHour == 0 {
		requestData.LunchStartHour = 12
	}
	if requestData.LunchEndHour == 0 {
		requestData.LunchEndHour = 13
	}

	// Parse the datetime strings
	startTime, err := time.Parse("2006-01-02T15:04:05", requestData.StartTime)
	if err != nil {
		http.Error(w, "Invalid start time format. Use ISO 8601 format: 2006-01-02T15:04:05", http.StatusBadRequest)
		return
	}

	endTime, err := time.Parse("2006-01-02T15:04:05", requestData.EndTime)
	if err != nil {
		http.Error(w, "Invalid end time format. Use ISO 8601 format: 2006-01-02T15:04:05", http.StatusBadRequest)
		return
	}

	if endTime.Before(startTime) {
		http.Error(w, "End time must be after start time", http.StatusBadRequest)
		return
	}

	// Calculate working hours
	workingHours, workingDays, lunchDeducted := calculateWorkingHours(
		startTime,
		endTime,
		requestData.WorkStartHour,
		requestData.WorkEndHour,
		requestData.LunchStartHour,
		requestData.LunchEndHour,
		requestData.DeductLunch,
	)

	// Calculate total days
	totalDays := int(endTime.Sub(startTime).Hours()/24) + 1

	response := WorkingHoursResponse{
		StartTime:     requestData.StartTime,
		EndTime:       requestData.EndTime,
		WorkingHours:  workingHours,
		TotalDays:     totalDays,
		WorkingDays:   workingDays,
		LunchDeducted: lunchDeducted,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func calculateWorkingHours(
	start, end time.Time,
	workStart, workEnd int,
	lunchStart, lunchEnd int,
	deductLunch bool,
) (float64, int, float64) {
	totalHours := 0.0
	workingDays := 0
	lunchDeducted := 0.0

	// Iterate through each day
	current := start
	for current.Before(end) || current.Equal(end) {
		// Check if it's a weekday (Monday to Friday)
		if current.Weekday() >= time.Monday && current.Weekday() <= time.Friday {
			dayStart := time.Date(current.Year(), current.Month(), current.Day(), workStart, 0, 0, 0, current.Location())
			dayEnd := time.Date(current.Year(), current.Month(), current.Day(), workEnd, 0, 0, 0, current.Location())

			// Determine the actual work start and end for this day
			actualStart := maxTime(start, dayStart)
			actualEnd := minTime(end, dayEnd)

			// If there's overlap with working hours
			if actualStart.Before(actualEnd) {
				workingDays++
				hours := actualEnd.Sub(actualStart).Hours()

				// Deduct lunch if enabled and the day spans lunch time
				if deductLunch {
					lunchStartTime := time.Date(current.Year(), current.Month(), current.Day(), lunchStart, 0, 0, 0, current.Location())
					lunchEndTime := time.Date(current.Year(), current.Month(), current.Day(), lunchEnd, 0, 0, 0, current.Location())

					// Check if work hours overlap with lunch hours
					if actualStart.Before(lunchEndTime) && actualEnd.After(lunchStartTime) {
						// Calculate lunch overlap
						lunchOverlapStart := maxTime(actualStart, lunchStartTime)
						lunchOverlapEnd := minTime(actualEnd, lunchEndTime)
						
						if lunchOverlapStart.Before(lunchOverlapEnd) {
							lunchHours := lunchOverlapEnd.Sub(lunchOverlapStart).Hours()
							hours -= lunchHours
							lunchDeducted += lunchHours
						}
					}
				}

				totalHours += hours
			}
		}

		// Move to the next day
		current = time.Date(current.Year(), current.Month(), current.Day()+1, 0, 0, 0, 0, current.Location())
	}

	return totalHours, workingDays, lunchDeducted
}

func maxTime(a, b time.Time) time.Time {
	if a.After(b) {
		return a
	}
	return b
}

func minTime(a, b time.Time) time.Time {
	if a.Before(b) {
		return a
	}
	return b
}
