# Curso de Programación de Software

## Descripción del Curso
Material completo del curso de Programación de Software organizado por módulos para facilitar el aprendizaje. Cada módulo incluye teoría detallada, ejemplos prácticos, ejercicios resueltos y casos de uso del mundo real.

## Estructura del Curso

### [Módulo 1: Introducción a POO en Python](./01-Introduccion-POO-Python/)
- **Teoría completa** con analogías del mundo real
- **Conceptos fundamentales**: Clases, objetos, atributos, métodos
- **Principios POO**: Encapsulación, herencia, polimorfismo
- **Sistema completo** de gestión de vehículos
- **Ejercicios prácticos** con soluciones detalladas
- **Ejemplos ejecutables** paso a paso

### [Módulo 2: Ejemplo de Examen](./02-Ejemplo-examen-1/)
- **Sistema bancario completo** con herencia
- **Clases**: Cliente, Cuenta, CuentaAhorro, CuentaCorriente
- **Implementación de POO** en un caso real
- **Ejemplo de examen** con solución completa

### [Módulo 3: Introducción a ORM con FastAPI](./03-Introduccion-ORM%20con%20fastAPI/)
- **Backend completo** con FastAPI y SQLAlchemy
- **ORM**: Mapeo objeto-relacional con SQLAlchemy
- **API REST**: Endpoints para usuarios, categorías y productos
- **Autenticación**: Sistema de login y registro
- **Base de datos**: Migraciones con Alembic

### [Módulo 4: Frontend Angular](./04-Frontend-angular/)
- **Frontend moderno** con Angular 17+
- **Arquitectura limpia** con standalone components
- **Sidebar responsivo** con navegación
- **Componentes reutilizables** y servicios
- **Integración con backend** FastAPI

## Cómo Crear el Sidebar en Angular - Paso a Paso

### 1. Crear la Estructura de Carpetas
```bash
mkdir -p src/app/shared/components/sidebar
```

### 2. Crear el Componente TypeScript
**Archivo**: `src/app/shared/components/sidebar/sidebar.component.ts`
```typescript
import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';

declare interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}

export const ROUTES: RouteInfo[] = [
    { path: '/dashboard', title: 'Dashboard',  icon: 'design_app', class: '' },
    { path: '/categorias', title: 'Categorías',  icon:'shopping_basket', class: '' },
    { path: '/usuarios', title: 'Usuarios',  icon:'users_single-02', class: '' },
    { path: '/productos', title: 'Productos',  icon:'shopping_box', class: '' },
    { path: '/notifications', title: 'Notificaciones',  icon:'ui-1_bell-53', class: '' },
    { path: '/upgrade', title: 'Configuración',  icon:'objects_spaceship', class: 'active active-pro' }
];

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  menuItems: any[] = [];

  constructor() { }

  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
  
  isMobileMenu() {
      if ( window.innerWidth > 991) {
          return false;
      }
      return true;
  };
}
```

### 3. Crear el Template HTML
**Archivo**: `src/app/shared/components/sidebar/sidebar.component.html`
```html
<div class="logo">
    <a href="#" class="simple-text logo-mini">
      <div class="logo-img">
          <div class="logo-text">ITM</div>
      </div>
    </a>
    <a href="#" class="simple-text logo-normal">
        Sistema ITM
    </a>
</div>
<div class="sidebar-wrapper">
    <ul class="nav">
        <li routerLinkActive="active" *ngFor="let menuItem of menuItems" class="{{menuItem.class}} nav-item">
            <a [routerLink]="[menuItem.path]">
                <i class="now-ui-icons {{menuItem.icon}}"></i>
                <p>{{menuItem.title}}</p>
            </a>
        </li>
    </ul>
</div>
```

### 4. Crear los Estilos SCSS
**Archivo**: `src/app/shared/components/sidebar/sidebar.component.scss`
```scss
// Sidebar styles
.sidebar {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 1000;
  width: 260px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.logo {
  padding: 15px 0;
  margin: 0;
  display: block;
  position: relative;
  z-index: 4;
}

.logo-img {
  width: 30px;
  height: 30px;
  display: inline-block;
  margin-left: 10px;
  margin-right: 15px;
  border-radius: 30px;
  text-align: center;
  overflow: hidden;
  vertical-align: middle;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  color: white;
  font-weight: bold;
  font-size: 12px;
  text-align: center;
}

.simple-text {
  padding: 5px 0px;
  display: block;
  white-space: nowrap;
  font-size: 14px;
  color: #fff;
  text-decoration: none;
  font-weight: 400;
  line-height: 30px;
  overflow: hidden;
}

.nav {
  margin-top: 20px;
  display: block;
}

.nav li {
  position: relative;
  display: block;
}

.nav li > a {
  color: #fff;
  display: block;
  text-decoration: none;
  position: relative;
  text-transform: uppercase;
  cursor: pointer;
  font-size: 12px;
  padding: 10px 8px;
  line-height: 30px;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.nav li > a:hover {
  background: rgba(255, 255, 255, 0.1);
  opacity: 1;
  color: #fff;
}

.nav li > a.active {
  background: rgba(255, 255, 255, 0.2);
  opacity: 1;
  color: #fff;
}

.nav li > a i {
  font-size: 20px;
  float: left;
  margin-right: 12px;
  line-height: 30px;
  width: 34px;
  text-align: center;
}

.nav li > a p {
  margin: 0;
  line-height: 30px;
  font-size: 14px;
  position: relative;
  display: block;
  height: auto;
  white-space: nowrap;
  transition: 0.3s ease;
}
```

### 5. Actualizar el App Component
**Archivo**: `src/app/app.component.ts`
```typescript
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';
import { SidebarComponent } from './shared/components/sidebar/sidebar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterModule, SidebarComponent],
  template: `
    <div class="wrapper">
      <div class="sidebar" data-color="red">
        <app-sidebar></app-sidebar>
      </div>
      <div class="main-panel">
        <div class="content">
          <router-outlet></router-outlet>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .wrapper {
      display: flex;
      min-height: 100vh;
    }

    .sidebar {
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      z-index: 1000;
      width: 260px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
    }

    .main-panel {
      flex: 1;
      margin-left: 260px;
      background: #f8f9fa;
      min-height: 100vh;
    }

    .content {
      padding: 0;
    }

    @media (max-width: 991px) {
      .sidebar {
        transform: translate3d(-260px, 0, 0);
        transition: all 0.33s cubic-bezier(0.685, 0.0473, 0.346, 1);
      }
      
      .sidebar.show {
        transform: translate3d(0, 0, 0);
      }
      
      .main-panel {
        margin-left: 0;
      }
    }
  `]
})
export class AppComponent {
  title = 'frontend-angular-clean-architecture';
}
```

### 6. Agregar Estilos Globales
**Archivo**: `src/styles.scss`
```scss
/* Simple text icons without emojis */
.now-ui-icons.design_app:before { content: "■"; }
.now-ui-icons.shopping_basket:before { content: "●"; }
.now-ui-icons.users_single-02:before { content: "▲"; }
.now-ui-icons.shopping_box:before { content: "◆"; }
.now-ui-icons.ui-1_bell-53:before { content: "○"; }
.now-ui-icons.objects_spaceship:before { content: "◊"; }
.now-ui-icons.ui-1_simple-add:before { content: "+"; }
.now-ui-icons.ui-2_settings-90:before { content: "●"; }
.now-ui-icons.ui-1_simple-remove:before { content: "×"; }
```

### 7. Configurar las Rutas
**Archivo**: `src/app/app.routes.ts`
```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./features/dashboard/dashboard.component').then(m => m.DashboardComponent)
  },
  {
    path: 'categorias',
    loadComponent: () => import('./features/categoria/categoria-list/categoria-list.component').then(m => m.CategoriaListComponent)
  },
  {
    path: 'productos',
    loadComponent: () => import('./features/producto/producto-list/producto-list.component').then(m => m.ProductoListComponent)
  },
  {
    path: 'usuarios',
    loadComponent: () => import('./features/usuario/usuario-list/usuario-list.component').then(m => m.UsuarioListComponent)
  }
];
```

### 8. Ejecutar la Aplicación
```bash
npm start
```

¡Listo! Ahora tienes un sidebar completamente funcional con navegación, estilos responsivos y integración con el sistema de rutas de Angular.

## Docente
**Alejandro Salgar Marín**  
Instituto Tecnológico Metropolitano (ITM)  
Período Académico: 2025-2

## Cómo Usar Este Repositorio

### **Para Estudiantes:**
1. **Clona el repositorio**: `git clone [URL]`
2. **Navega por módulos**: Comienza con el Módulo 1 y avanza secuencialmente
3. **Ejecuta ejemplos**: Cada módulo incluye código ejecutable
4. **Practica ejercicios**: Resuelve los ejercicios antes de ver las soluciones
5. **Experimenta**: Modifica el código y observa los cambios

### **Para Instructores:**
- **Material listo para usar**: Cada módulo está completo y autocontenido
- **Ejercicios graduados**: Dificultad progresiva desde básico hasta avanzado
- **Casos de uso reales**: Ejemplos aplicables a situaciones del mundo real
- **Flexibilidad**: Fácil de adaptar a diferentes estilos de enseñanza

## Características del Curso

- **Teoría Sólida**: Explicaciones claras con analogías del mundo real
- **Código Ejecutable**: Ejemplos que puedes correr y modificar
- **Ejercicios Prácticos**: Problemas reales con soluciones detalladas
- **Proyectos Completos**: Sistemas que integran múltiples conceptos
- **Documentación Clara**: Explicaciones paso a paso para cada concepto

---

*¡Bienvenidos al mundo de la programación! Este curso te llevará desde los fundamentos hasta la creación de aplicaciones complejas.*
