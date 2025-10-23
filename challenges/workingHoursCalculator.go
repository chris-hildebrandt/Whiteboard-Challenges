package challenges

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"time"
)

type WorkedHoursRequest struct {
	StartTime      string `json:"startTime"`
	EndTime        string `json:"endTime"`
	WorkStartHour  int    `json:"workStartHour"`
	WorkEndHour    int    `json:"workEndHour"`
	LunchStartHour int    `json:"lunchStartHour"`
	LunchEndHour   int    `json:"lunchEndHour"`
	DeductLunch    bool   `json:"deductLunch"`
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

	start, end, err := parseTimes(reqData.StartTime, reqData.EndTime)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	workingHours, workingDays, lunchDeducted := calculateWorkingHours(
		start, end,
		reqData.WorkStartHour, reqData.WorkEndHour,
		reqData.LunchStartHour, reqData.LunchEndHour,
		reqData.DeductLunch,
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

func parseTimes(startStr, endStr string) (time.Time, time.Time, error) {
	start, err := time.Parse(time.RFC3339, startStr)
	if err != nil {
		return time.Time{}, time.Time{}, errors.New("invalid startTime: must be ISO 8601")
	}

	end, err := time.Parse(time.RFC3339, endStr)
	if err != nil {
		return time.Time{}, time.Time{}, errors.New("invalid endTime: must be ISO 8601")
	}

	if end.Before(start) {
		return time.Time{}, time.Time{}, errors.New("endTime must be after startTime")
	}
	return start, end, nil
}

func calculateWorkingHours(
	start, end time.Time,
	workStart, workEnd, lunchStart, lunchEnd int,
	deductLunch bool,
) (totalHours float64, workingDays int, lunchDeducted float64) {

	for day := start; !day.After(end); day = day.AddDate(0, 0, 1) {
		if !isWeekday(day) {
			continue
		}

		dayStart := time.Date(day.Year(), day.Month(), day.Day(), workStart, 0, 0, 0, day.Location())
		dayEnd := time.Date(day.Year(), day.Month(), day.Day(), workEnd, 0, 0, 0, day.Location())

		actualStart := maxTime(start, dayStart)
		actualEnd := minTime(end, dayEnd)

		if !actualStart.Before(actualEnd) {
			continue
		}

		workingDays++
		hours := actualEnd.Sub(actualStart).Hours()

		if deductLunch {
			lunchStartTime := time.Date(day.Year(), day.Month(), day.Day(), lunchStart, 0, 0, 0, day.Location())
			lunchEndTime := time.Date(day.Year(), day.Month(), day.Day(), lunchEnd, 0, 0, 0, day.Location())
			lunchHours := overlapHours(actualStart, actualEnd, lunchStartTime, lunchEndTime)
			hours -= lunchHours
			lunchDeducted += lunchHours
		}

		totalHours += hours
	}
	return
}

func isWeekday(t time.Time) bool {
	return t.Weekday() >= time.Monday && t.Weekday() <= time.Friday
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
