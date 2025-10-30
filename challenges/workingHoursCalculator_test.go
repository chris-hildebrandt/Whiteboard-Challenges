package challenges

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestWorkingHoursCalculatorHandler(t *testing.T) {
	// Test cases for the handler
	tests := []struct {
		name           string
		in             *http.Request
		out            *httptest.ResponseRecorder
		expectedStatus int
		expectedBody   string
	}{
		{
			name: "good request",
			in: httptest.NewRequest("POST", "/work", bytes.NewBufferString(`{
				"startTime": "2025-10-27T09:00:00Z",
				"endTime": "2025-10-31T17:00:00Z",
				"workStartHour": 9,
				"workEndHour": 17,
				"lunchStartHour": 12,
				"lunchEndHour": 13,
				"deductLunch": true,
				"holidays": ["2025-10-29"]
			}`)),
			out:            httptest.NewRecorder(),
			expectedStatus: http.StatusOK,
			expectedBody:   `{"startTime":"2025-10-27T09:00:00Z","endTime":"2025-10-31T17:00:00Z","workingHours":28,"totalDays":5,"workingDays":4,"lunchDeducted":4}`,
		},
		{
			name:           "bad request method",
			in:             httptest.NewRequest("GET", "/work", nil),
			out:            httptest.NewRecorder(),
			expectedStatus: http.StatusMethodNotAllowed,
			expectedBody:   "Only POST method is allowed\n",
		},
		{
			name:           "invalid JSON",
			in:             httptest.NewRequest("POST", "/work", bytes.NewBufferString(`{"startTime":}`)),
			out:            httptest.NewRecorder(),
			expectedStatus: http.StatusBadRequest,
			expectedBody:   "invalid JSON format\n",
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			WorkingHoursCalculatorHandler(test.out, test.in)
			if test.out.Code != test.expectedStatus {
				t.Errorf("expected status %d, got %d", test.expectedStatus, test.out.Code)
			}

			if test.expectedStatus == http.StatusOK {
				var actual, expected WorkingHoursResponse
				if err := json.Unmarshal(test.out.Body.Bytes(), &actual); err != nil {
					t.Fatalf("could not unmarshal actual response: %v", err)
				}
				if err := json.Unmarshal([]byte(test.expectedBody), &expected); err != nil {
					t.Fatalf("could not unmarshal expected response: %v", err)
				}
				if actual != expected {
					t.Errorf("expected body %+v, got %+v", expected, actual)
				}
			} else {
				if test.out.Body.String() != test.expectedBody {
					t.Errorf("expected body %q, got %q", test.expectedBody, test.out.Body.String())
				}
			}
		})
	}
}

func TestCalculateWorkingHours(t *testing.T) {
	// Test cases for the calculation logic
	tests := []struct {
		name                string
		start               time.Time
		end                 time.Time
		workStart           int
		workEnd             int
		lunchStart          int
		lunchEnd            int
		deductLunch         bool
		holidays            []string
		expectedHours       float64
		expectedWorkingDays int
		expectedLunch       float64
	}{
		{
			name:                "single day, no lunch",
			start:               time.Date(2025, 10, 27, 9, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 17, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			deductLunch:         false,
			expectedHours:       8,
			expectedWorkingDays: 1,
			expectedLunch:       0,
		},
		{
			name:                "single day, with lunch",
			start:               time.Date(2025, 10, 27, 9, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 17, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			lunchStart:          12,
			lunchEnd:            13,
			deductLunch:         true,
			expectedHours:       7,
			expectedWorkingDays: 1,
			expectedLunch:       1,
		},
		{
			name:                "multiple days, with lunch",
			start:               time.Date(2025, 10, 27, 9, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 28, 17, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			lunchStart:          12,
			lunchEnd:            13,
			deductLunch:         true,
			expectedHours:       14,
			expectedWorkingDays: 2,
			expectedLunch:       2,
		},
		{
			name:                "with weekend",
			start:               time.Date(2025, 10, 24, 9, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 17, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			lunchStart:          12,
			lunchEnd:            13,
			deductLunch:         true,
			expectedHours:       14,
			expectedWorkingDays: 2,
			expectedLunch:       2,
		},
		{
			name:                "with holiday",
			start:               time.Date(2025, 10, 27, 9, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 28, 17, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			lunchStart:          12,
			lunchEnd:            13,
			deductLunch:         true,
			holidays:            []string{"2025-10-28"},
			expectedHours:       7,
			expectedWorkingDays: 1,
			expectedLunch:       1,
		},
		{
			name:                "start and end outside working hours",
			start:               time.Date(2025, 10, 27, 8, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 18, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			lunchStart:          12,
			lunchEnd:            13,
			deductLunch:         true,
			expectedHours:       7,
			expectedWorkingDays: 1,
			expectedLunch:       1,
		},
		{
			name:                "partial overlap start",
			start:               time.Date(2025, 10, 27, 8, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 10, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			deductLunch:         true,
			expectedHours:       1,
			expectedWorkingDays: 1,
			expectedLunch:       0,
		},
		{
			name:                "partial overlap end",
			start:               time.Date(2025, 10, 27, 16, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 18, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			deductLunch:         true,
			expectedHours:       1,
			expectedWorkingDays: 1,
			expectedLunch:       0,
		},
		{
			name:                "no overlap",
			start:               time.Date(2025, 10, 27, 18, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 27, 19, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			deductLunch:         true,
			expectedHours:       0,
			expectedWorkingDays: 0,
			expectedLunch:       0,
		},
		{
			name:                "start and end on weekend",
			start:               time.Date(2025, 10, 25, 9, 0, 0, 0, time.UTC),
			end:                 time.Date(2025, 10, 26, 17, 0, 0, 0, time.UTC),
			workStart:           9,
			workEnd:             17,
			deductLunch:         true,
			expectedHours:       0,
			expectedWorkingDays: 0,
			expectedLunch:       0,
		},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			hours, days, lunch := calculateWorkingHours(
				test.start, test.end,
				test.workStart, test.workEnd,
				test.lunchStart, test.lunchEnd,
				test.deductLunch, test.holidays,
			)
			if hours != test.expectedHours {
				t.Errorf("expected hours %.2f, got %.2f", test.expectedHours, hours)
			}
			if days != test.expectedWorkingDays {
				t.Errorf("expected working days %d, got %d", test.expectedWorkingDays, days)
			}
			if lunch != test.expectedLunch {
				t.Errorf("expected lunch %.2f, got %.2f", test.expectedLunch, lunch)
			}
		})
	}
}