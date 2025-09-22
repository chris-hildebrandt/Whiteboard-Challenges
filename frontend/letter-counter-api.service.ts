import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LetterCounterApiService {

  // The URL to your Go backend endpoint.
  // We'll use the proxy config to forward this to http://localhost:8080/letterCounter
  private apiUrl = '/api/letterCounter';

  constructor(private http: HttpClient) { }

  countLetters(text: string): Observable<any> {
    return this.http.post(this.apiUrl, { input: text });
  }
}