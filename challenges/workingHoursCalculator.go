package challenges

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"time"
)

type WorkedHoursRequest struct {
	StartTime      string   `json:"startTime"`
	EndTime        string   `json:"endTime"`
	WorkStartHour  int      `json:"workStartHour"`
	WorkEndHour    int      `json:"workEndHour"`
	LunchStartHour int      `json:"lunchStartHour"`
	LunchEndHour   int      `json:"lunchEndHour"`
	DeductLunch    bool     `json:"deductLunch"`
	Holidays       []string `json:"holidays,omitempty"`
}

type WorkingHoursResponse struct {
	StartTime     string  `json:"startTime"`
	EndTime       string  `json:"endTime"`
	WorkingHours  float64 `json:"workingHours"`
	TotalDays     int     `json:"totalDays"`
	WorkingDays   int     `json:"workingDays"`
	LunchDeducted float64 `json:"lunchDeducted"`
}

func WorkingHoursCalculatorHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}
	defer r.Body.Close()

	reqData, err := parseRequest(r.Body)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	start, err := time.Parse(time.RFC3339, reqData.StartTime)
	if err != nil {
		http.Error(w, "invalid startTime format: use ISO 8601", http.StatusBadRequest)
		return
	}

	end, err := time.Parse(time.RFC3339, reqData.EndTime)
	if err != nil {
		http.Error(w, "invalid endTime format: use ISO 8601", http.StatusBadRequest)
		return
	}

	if !start.Before(end) {
		http.Error(w, "endTime must be after startTime", http.StatusBadRequest)
		return
	}

	workingHours, workingDays, lunchDeducted := calculateWorkingHours(
		start, end,
		reqData.WorkStartHour, reqData.WorkEndHour,
		reqData.LunchStartHour, reqData.LunchEndHour,
		reqData.DeductLunch,
		reqData.Holidays,
	)

	totalDays := int(end.Sub(start).Hours()/24) + 1

	response := WorkingHoursResponse{
		StartTime:     reqData.StartTime,
		EndTime:       reqData.EndTime,
		WorkingHours:  workingHours,
		TotalDays:     totalDays,
		WorkingDays:   workingDays,
		LunchDeducted: lunchDeducted,
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(response)
}

func parseRequest(body io.Reader) (WorkedHoursRequest, error) {
	var data WorkedHoursRequest
	if err := json.NewDecoder(body).Decode(&data); err != nil {
		return data, errors.New("invalid JSON format")
	}
	return data, nil
}

func calculateWorkingHours(
	start, end time.Time,
	workStart, workEnd, lunchStart, lunchEnd int,
	deductLunch bool,
	holidays []string,
) (float64, int, float64) {
	totalHours := 0.0
	workingDays := 0
	totalLunchDeducted := 0.0

	current := start
	for current.Before(end) || current.Equal(end) {
		dayStart := time.Date(current.Year(), current.Month(), current.Day(), 0, 0, 0, 0, current.Location())

		if isWeekend(dayStart) || isHoliday(dayStart, holidays) {
			current = current.AddDate(0, 0, 1)
			continue
		}

		workDayStart := time.Date(current.Year(), current.Month(), current.Day(), workStart, 0, 0, 0, current.Location())
		workDayEnd := time.Date(current.Year(), current.Month(), current.Day(), workEnd, 0, 0, 0, current.Location())

		periodStart := maxTime(start, workDayStart)
		periodEnd := minTime(end, workDayEnd)

		if periodStart.Before(periodEnd) {
			hours := periodEnd.Sub(periodStart).Hours()

			if deductLunch {
				lunchStartTime := time.Date(current.Year(), current.Month(), current.Day(), lunchStart, 0, 0, 0, current.Location())
				lunchEndTime := time.Date(current.Year(), current.Month(), current.Day(), lunchEnd, 0, 0, 0, current.Location())
				lunchHours := overlapHours(periodStart, periodEnd, lunchStartTime, lunchEndTime)
				hours -= lunchHours
				totalLunchDeducted += lunchHours
			}

			totalHours += hours
			workingDays++
		}

		current = current.AddDate(0, 0, 1)
	}

	return totalHours, workingDays, totalLunchDeducted
}

func isWeekend(t time.Time) bool {
	return t.Weekday() == time.Saturday || t.Weekday() == time.Sunday
}

func isHoliday(t time.Time, holidays []string) bool {
	dateStr := t.Format("2006-01-02")
	for _, h := range holidays {
		if h == dateStr {
			return true
		}
	}
	return false
}

func overlapHours(aStart, aEnd, bStart, bEnd time.Time) float64 {
	start := maxTime(aStart, bStart)
	end := minTime(aEnd, bEnd)
	if start.Before(end) {
		return end.Sub(start).Hours()
	}
	return 0
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