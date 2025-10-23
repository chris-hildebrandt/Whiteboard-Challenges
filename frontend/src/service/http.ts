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
    // ... (error handling)
    return throwError(() => new Error(error.error?.message || error.statusText || 'An unknown error occurred'));
  }

  post<T>(endpoint: string, body: unknown): Observable<T> {
    // ⬇️ this was the source of my CORS error: The Cross-Origin Resource Sharing (CORS) error is occurring because the Go server, which hosts the API on port 8080, is not sending the necessary Access-Control-Allow-Origin header in its response to the client running on port 4200. Although the Go code has an enableCORS middleware, the API Service in the Angular application is bypassing the proxy and making a direct request to the 8080 URL, which is not set up to handle the specific origin from the hosting environment.
    // return this.http.post<T>(`https://verbose-guacamole-qjv9p67j95634vr-8080.app.github.dev/${endpoint}`, body).pipe( 
    return this.http.post<T>(`/api/${endpoint}`, body).pipe(
      catchError(this.handleError)
    );
  }

  get<T>(endpoint: string): Observable<T> {
    // This method already uses the proxy correctly:
    return this.http.get<T>(`/api/${endpoint}`).pipe(
      catchError(this.handleError)
    );
  }
}