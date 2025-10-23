import { Component, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
    // Set default dates
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
    return `${date}T${time}:00`;
  }

  calculateWorkingHours() {
    this.errorMessage = '';
    this.result = null;

    if (!this.startDate || !this.startTime || !this.endDate || !this.endTime) {
      this.errorMessage = 'Please fill in all date and time fields';
      return;
    }

    const startDateTime = this.formatDateTime(this.startDate, this.startTime);
    const endDateTime = this.formatDateTime(this.endDate, this.endTime);

    // Validate that end is after start
    if (new Date(endDateTime) <= new Date(startDateTime)) {
      this.errorMessage = 'End date/time must be after start date/time';
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
        this.result = response;
        this.isCalculating = false;
      },
      error: (error) => {
        this.errorMessage = error.message || 'An error occurred while calculating working hours';
        this.isCalculating = false;
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
  }
}
