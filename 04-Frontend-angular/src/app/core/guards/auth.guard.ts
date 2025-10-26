import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    // Si no está autenticado, redirigir al login
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/auth/login']);
      return false;
    }

    // Obtener la ruta de destino
    const targetRoute = route.routeConfig?.path || '';
    
    // Verificar si el usuario puede acceder a la ruta
    if (!this.authService.canAccess(targetRoute)) {
      // Si no puede acceder, redirigir al dashboard o a una página de error
      this.router.navigate(['/dashboard']);
      return false;
    }

    return true;
  }
}
