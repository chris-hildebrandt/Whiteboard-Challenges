import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private http = inject(HttpClient);

  private handleError(error: HttpErrorResponse) {
    console.error('API Error:', error);
    return throwError(() => new Error(error.error?.message || error.statusText || 'An unknown error occurred'));
  }

  post<T>(endpoint: string, body: unknown): Observable<T> {
    return this.http.post<T>(`https://verbose-guacamole-qjv9p67j95634vr-8080.app.github.dev/${endpoint}`, body).pipe(
      catchError(this.handleError)
    );
  }

  get<T>(endpoint: string): Observable<T> {
    return this.http.get<T>(`/api/${endpoint}`).pipe(
      catchError(this.handleError)
    );
  }
}
