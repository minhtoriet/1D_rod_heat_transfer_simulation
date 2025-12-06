# 1-Dimensional heat transfer simulation app
## Introduction
Hi folks!  Just like what the title suggests  (hope you have an idea of what that is before coming to us).  This app lets you skip any kind of abstraction  (by abstracting and basically ignoring the 2D properties of an actual rod) and gets straight  to seeing how heat eventually redistribute and come to an equilibrium after some time.

1. You can refer to the following material for our numerical approach for the app: [Introduction to Numerical Methods in Heat Transfer](https://ntrs.nasa.gov/api/citations/20200006182/downloads/Introduction%20to%20Numerical%20Methods%20in%20Heat%20Transfer.pdf).

2. As well as consulting this for an analytical solution for such problem:  [The One-Dimensional Heat Equation](http://ramanujan.math.trinity.edu/rdaileda/teach/s17/m3357/lectures/lecture9.pdf).

## Explaination
Imagine heating up a metal rod.  You can control the temperature of the rod at a certain length, like heating up in one place while cooling down another.  Then you stop changing heat on the rod and starts counting time.  We represent different spots on the rod of length $L$ at time $t$ by $x \in [0,L]$, with temperature $u(x,t)$

![rod](https://iu.pressbooks.pub/app/uploads/sites/1316/2023/11/Heat-conduction.svg-300x151.png)  

However, solving such problem is known to be difficult. Therefore, choosing a boundary condition is just as important as solving the problem itself, as it makes the problem more digestible while focusing on the most important point.  Details of some BCs will be listed in the following part.  [A boundary conditions are constraints necessary for the solution of a boundary value problem](https://www.simscale.com/docs/simwiki/numerics-background/what-are-boundary-conditions/).  In this case, BCs are applied to two heads of the rod.

## Basics
1. We solve the one-dimensional heat (diffusion) equation on a rod of length 𝐿:    
```math
\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2}, \qquad x \in (0,L),\; t>0.
```
where $u(x,t)$ is temperature, $\alpha$ is the thermal diffusivity (unit: $length^2/time$).  

2. This PDE is supplied with:
   - An initial temperature profile $u(x,t) = u_0(x)$
   - Boundary conditions:
       + Dirichlet (fixed temperature at two rod heads) $u(0,t) = T_0,\; u(L,t) = T_L\$
       + Neumann (insulated heads) $\\partial_x u(0,t) = 0\$
    
3.There are analytical solutions for such problem:
   - For Dirichlet boundary,  
```math
u(x,t) = \sum_{n=1}^{\infty} u_n(x,t) 
       = \sum_{n=1}^{\infty} b_n e^{-\lambda_n^2 t} \sin(\mu_n x)
```
  - With the sine series expansion of $f(x)$:  
```math
f(x) = u(x,0) = \sum_{n=1}^{\infty} b_n \sin\left( \frac{n\pi x}{L} \right)
```
  - Hence
```math
b_n = \frac{2}{L} \int_0^L f(x)\, \sin\left( \frac{n\pi x}{L} \right)\, dx
```
Which is perfect for confirming results - it is **exact**, after all.  But such lengthy equation is also **expensive** to compute (who would have guessed!1!1!!).  Therefore, most realistic use cases of this problem requires numerical methods, which is what this project demonstrates.  

## Approach  
1. Divide the rod into a spatial grid: $x_i = i \Delta x, i = 0...N$
2. Time levels: $t^n = n\Delta t$
3. Let $u^n_i$ approximate $u(x_i,t^n)$, and define
```math
r = \frac{\alpha\Delta t}{2(\Delta x)^2}
```
Crank–Nicolson applies centered second differences in space and averages between time levels $n$ and $n+1$. The resulting set of equations for interior nodes $i = 1...N$ is 
```math
- r\,u_{i-1}^{\,n+1} + (1 + 2r)\,u_{i}^{\,n+1} - r\,u_{i+1}^{\,n+1}
= r\,u_{i-1}^{\,n} + (1 - 2r)\,u_{i}^{\,n} + r\,u_{i+1}^{\,n}.
```
Which can be solved via a tridiagonal linear system $Au^{n+1} = b$ at each time step (time complexity $O(n)$ using Thomas algorithm).  

 4. Boundary conditions will be implemented differently on the first and last row of the tridiagonal matrix

> refer to [this](https://www.math.ntnu.no/emner/TMA4135/2015h/notater/crank-nicolson/cn.pdf) for the derivation of Crank-Nicolson method (I don't get it either). 

## Demo
![Recording 2025-12-06 142026.gif](https://github.com/minhtoriet/1D_rod_heat_transfer_simulation/blob/main/Recording%202025-12-06%20142026.gif)

