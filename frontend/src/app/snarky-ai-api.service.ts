import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SnarkyAiApiService {

  private apiUrl = '/api/snarky';

  constructor(private http: HttpClient) { }

  getOpeningPrompt(): Observable<{ prompt: string }> {
    return this.http.get<{ prompt: string }>(`${this.apiUrl}/prompt`);
  }

  getResponse(userInput: string): Observable<{ response: string }> {
    return this.http.post<{ response: string }>(this.apiUrl, { input: userInput });
  }
}
