import { Component } from '@angular/core';
import { LetterCounterApiService } from 'frontend/letter-counter-api.service';

@Component({
  selector: 'app-letter-counter',
  templateUrl: './letter-counter.component.html',
  styleUrls: ['./letter-counter.component.css']
})
export class LetterCounterComponent {
  userInput: string = 'Hello, World!'; // Default input text
  apiResponse: any = null; // To store the response from the backend
  errorMessage: string | null = null;

  // Inject the API service
  constructor(private apiService: LetterCounterApiService) {}

  // This function will be called when the user clicks the button
  getLetterCounts() {
    this.errorMessage = null;
    this.apiResponse = null;
    this.apiService.countLetters(this.userInput).subscribe({
      next: (data) => {
        this.apiResponse = data;
      },
      error: (err) => {
        this.errorMessage = 'Failed to connect to the backend. Is it running?';
        console.error(err);
      }
    });
  }
}