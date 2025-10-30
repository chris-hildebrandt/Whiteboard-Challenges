import { Component, inject, ChangeDetectorRef, OnInit, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { NgIf, NgFor, NgClass } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SnarkyAiApiService } from './snarky-ai-api.service';

interface Message {
  text: string;
  sender: 'user' | 'ai';
}

@Component({
  selector: 'app-snarky-ai',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule],
  templateUrl: './snarky-ai.component.html',
  styleUrls: ['./snarky-ai.component.css']
})
export class SnarkyAiComponent implements OnInit, AfterViewChecked {
  private apiService = inject(SnarkyAiApiService);
  private cdr = inject(ChangeDetectorRef);

  @ViewChild('chatBox') private chatBoxContainer!: ElementRef;
  @ViewChild('promptInput') private promptInput!: ElementRef;

  openingPrompt: string | null = null;
  messages: Message[] = [];
  userInput = '';
  isThinking = false;
  errorMessage = '';

  ngOnInit() {
    this.isThinking = true;
    this.apiService.getOpeningPrompt().subscribe({
      next: (response) => {
        this.openingPrompt = response.prompt;
        this.isThinking = false;
        this.cdr.detectChanges();
        setTimeout(() => this.focusInput(), 0);
      },
      error: (error) => {
        this.errorMessage = 'Failed to get opening prompt. Is the server running?';
        this.isThinking = false;
        this.cdr.detectChanges();
      }
    });
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  sendMessage(event: Event) {
    event.preventDefault();
    const trimmedInput = this.userInput.trim();
    if (!trimmedInput || this.isThinking) {
      return;
    }

    this.messages.push({ text: trimmedInput, sender: 'user' });
    this.userInput = '';
    this.isThinking = true;
    this.errorMessage = '';

    this.apiService.getResponse(trimmedInput).subscribe({
      next: (response) => {
        this.messages.push({ text: response.response, sender: 'ai' });
        this.isThinking = false;
        this.cdr.detectChanges();
        this.focusInput();
      },
      error: (error) => {
        this.errorMessage = 'The AI is having a moment. Try again later.';
        this.isThinking = false;
        this.cdr.detectChanges();
      }
    });
  }

  private scrollToBottom(): void {
    try {
      this.chatBoxContainer.nativeElement.scrollTop = this.chatBoxContainer.nativeElement.scrollHeight;
    } catch(err) { }
  }

  private focusInput(): void {
    try {
      this.promptInput.nativeElement.focus();
    } catch(err) { }
  }
}
