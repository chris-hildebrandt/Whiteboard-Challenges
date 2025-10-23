import { Component, inject, ChangeDetectorRef } from '@angular/core';
import { NgIf, DecimalPipe, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../service/http';

interface WorkingHoursRequest {
  startTime: string;
  endTime: string;
  workStartHour: number;
  workEndHour: number;
  lunchStartHour: number;
  lunchEndHour: number;
  deductLunch: boolean;
}

interface WorkingHoursResponse {
  startTime: string;
  endTime: string;
  workingHours: number;
  totalDays: number;
  workingDays: number;
  lunchDeducted: number;
}

@Component({
  selector: 'app-working-hours-calculator',
  standalone: true,
  imports: [NgIf, FormsModule, DecimalPipe, DatePipe],
  templateUrl: './working-hours-calculator.component.html',
  styleUrl: './working-hours-calculator.component.css'
})
export class WorkingHoursCalculatorComponent {
  private apiService = inject(ApiService);
  private cdr = inject(ChangeDetectorRef);

  // Form inputs
  startDate = '';
  startTime = '09:00';
  endDate = '';
  endTime = '17:00';
  
  // Configuration options
  workStartHour = 9;
  workEndHour = 17;
  lunchStartHour = 12;
  lunchEndHour = 13;
  deductLunch = false;
  
  // Results
  result: WorkingHoursResponse | null = null;
  errorMessage = '';
  isCalculating = false;
  showAdvancedOptions = false;

  constructor() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    this.startDate = this.formatDate(today);
    this.endDate = this.formatDate(tomorrow);
  }

  formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }

  formatDateTime(date: string, time: string): string {
    return `${date}T${time}:00Z`;
  }

  // Sync startTime with workStartHour
  onStartTimeChange() {
    const hour = this.parseHourFromTime(this.startTime);
    if (hour !== null) {
      this.workStartHour = hour;
    }
  }

  // Sync endTime with workEndHour
  onEndTimeChange() {
    const hour = this.parseHourFromTime(this.endTime);
    if (hour !== null) {
      this.workEndHour = hour;
    }
  }

  // Sync workStartHour with startTime
  onWorkStartHourChange() {
    this.startTime = this.formatTimeFromHour(this.workStartHour);
  }

  // Sync workEndHour with endTime
  onWorkEndHourChange() {
    this.endTime = this.formatTimeFromHour(this.workEndHour);
  }

  parseHourFromTime(time: string): number | null {
    const parts = time.split(':');
    if (parts.length >= 1) {
      const hour = parseInt(parts[0], 10);
      if (!isNaN(hour) && hour >= 0 && hour <= 23) {
        return hour;
      }
    }
    return null;
  }

  formatTimeFromHour(hour: number): string {
    return `${hour.toString().padStart(2, '0')}:00`;
  }

  calculateWorkingHours() {
    this.errorMessage = '';
    this.result = null;

    console.log('--- Calculation Started ---');
    console.log('Input Data (Raw Component State):', {
        startDate: this.startDate,
        startTime: this.startTime,
        endDate: this.endDate,
        endTime: this.endTime
    });

    if (!this.startDate || !this.startTime || !this.endDate || !this.endTime) {
      this.errorMessage = 'Please fill in all date and time fields';
      console.error('Validation Failed: Missing fields.');
      return;
    }

    const startDateTime = this.formatDateTime(this.startDate, this.startTime);
    const endDateTime = this.formatDateTime(this.endDate, this.endTime);

    console.log('Formatted ISO Times (Sent to API):', {
        startDateTime: startDateTime,
        endDateTime: endDateTime
    });

    if (new Date(endDateTime) <= new Date(startDateTime)) {
      this.errorMessage = 'End date/time must be after start date/time';
      console.error('Validation Failed: End <= Start.');
      return;
    }

    this.isCalculating = true;

    const request: WorkingHoursRequest = {
      startTime: startDateTime,
      endTime: endDateTime,
      workStartHour: this.workStartHour,
      workEndHour: this.workEndHour,
      lunchStartHour: this.lunchStartHour,
      lunchEndHour: this.lunchEndHour,
      deductLunch: this.deductLunch
    };

    this.apiService.post<WorkingHoursResponse>('workingHoursCalculator', request).subscribe({
      next: (response) => {
        console.log('API Success Response:', response);
        console.log('--- Calculation Finished Successfully ---');
        setTimeout(() => {
            this.result = response;
            this.isCalculating = false;
            this.cdr.detectChanges();
        }, 0);
      },
      error: (error) => {
        this.errorMessage = error.message || 'An error occurred while calculating working hours';
        this.isCalculating = false;
        this.cdr.detectChanges();
        console.error('API Error Response:', error);
        console.log('--- Calculation Finished with Error ---');
      }
    });
  }

  toggleAdvancedOptions() {
    this.showAdvancedOptions = !this.showAdvancedOptions;
  }

  resetToDefaults() {
    this.workStartHour = 9;
    this.workEndHour = 17;
    this.lunchStartHour = 12;
    this.lunchEndHour = 13;
    this.deductLunch = false;
    this.startTime = '09:00';
    this.endTime = '17:00';
  }

  setQuickRange(days: number) {
    const start = new Date();
    start.setHours(9, 0, 0, 0);
    
    const end = new Date();
    end.setDate(end.getDate() + days);
    end.setHours(17, 0, 0, 0);

    this.startDate = this.formatDate(start);
    this.startTime = '09:00';
    this.endDate = this.formatDate(end);
    this.endTime = '17:00';
    this.workStartHour = 9;
    this.workEndHour = 17;
  }
}