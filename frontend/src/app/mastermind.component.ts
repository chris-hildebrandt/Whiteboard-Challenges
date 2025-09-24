import { Component, inject, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgFor, NgIf, NgClass } from '@angular/common';

interface Guess {
  pegs: string[];
  feedback: { hits: number; blows: number; };
}

@Component({
  selector: 'app-mastermind',
  standalone: true,
  imports: [NgFor, NgIf, NgClass],
  templateUrl: './mastermind.component.html',
  styleUrl: './mastermind.component.css'
})
export class MastermindComponent implements OnInit {
  private http = inject(HttpClient);

  availableColors: string[] = [];
  currentGuess: string[] = Array(4).fill('');
  guessHistory: Guess[] = [];
  message = '';
  isWinner = false;

  ngOnInit() {
    this.startNewGame();
  }

  startNewGame() {
    this.http.get<{ colors: string[], message: string }>('/api/mastermind').subscribe(response => {
      this.availableColors = response.colors;
      this.message = response.message;
      this.guessHistory = [];
      this.currentGuess = Array(4).fill('');
      this.isWinner = false;
    });
  }

  selectColor(color: string, index: number) {
    if (!this.isWinner) {
      this.currentGuess[index] = color;
    }
  }

  submitGuess() {
    if (this.currentGuess.includes('') || this.isWinner) {
      return; // Do not submit incomplete guesses or after winning
    }

    this.http.post<{ hits: number, blows: number }>('/api/mastermind/guess', { guess: this.currentGuess }).subscribe(feedback => {
      this.guessHistory.push({ pegs: [...this.currentGuess], feedback });

      if (feedback.hits === 4) {
        this.isWinner = true;
        this.message = 'Congratulations, you cracked the code!';
      } else {
        this.message = 'Incorrect. Try again!';
      }
      this.currentGuess = Array(4).fill('');
    });
  }
}