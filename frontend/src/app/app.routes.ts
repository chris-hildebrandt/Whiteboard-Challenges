import { Routes } from '@angular/router';

export const appRoutes: Routes = [
  {
    path: 'mastermind',
    loadComponent: () => import('./mastermind.component').then(m => m.MastermindComponent)
  },
  {
    path: '',
    redirectTo: '/mastermind',
    pathMatch: 'full'
  }];
