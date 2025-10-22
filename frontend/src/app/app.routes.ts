import { Routes } from '@angular/router';

export const appRoutes: Routes = [
  {
    path: 'mastermind',
    loadComponent: () => import('./mastermind.component').then(m => m.MastermindComponent)
  },
  {
    path: 'working-hours',
    loadComponent: () => import('./working-hours-calculator.component').then(m => m.WorkingHoursCalculatorComponent)
  },
  {
    path: '',
    redirectTo: '/working-hours',
    pathMatch: 'full'
  }];
