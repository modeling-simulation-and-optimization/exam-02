%{
    Exam 2
    Exercise 3

    Made by:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
%}

clc, clear all, close all;

syms z x y;

z = (1 - x)^2 + 100 * (y - x^2)^2;

figure
ezsurf(x, y, z)
hold on;

x_i = 0;
y_i = 10;
a = 0.1;
convergence = 0.001;

grad_z = gradient(z);
hess_z = hessian(z);

grad_z_eval = double(subs(grad_z, [x y], [x_i y_i]));

while abs(grad_z_eval) > convergence
    hessian_z_eval = double(subs(hess_z, [x y], [x_i y_i])); % Hessian evaluated in x_i, y_i
    grad_z_eval = double(subs(grad_z, [x y], [x_i y_i])); % Gradient evaluated in x_i, y_i
    z_i = [x_i; y_i];

    z_i_new = z_i - a * (inv(hessian_z_eval)) * grad_z_eval; % Newton Raphson expression

    x_i = z_i_new(1); % Update x_i
    y_i = z_i_new(2); % Update y_i

    z_eval = double(subs(z, [x y], [x_i y_i])); % Evaluate z in x_i, y_i to plot the result

    plot3(x_i, y_i, z_eval, '.', 'MarkerFaceColor', 'cyan', 'Color', 'cyan');
end

plot3(x_i, y_i, z_eval, 'o', 'MarkerFaceColor', 'red', 'Color', 'red', 'MarkerSize', 10);
text(-4, 10, 2 * 10^5, ['Global Min: (', num2str(x_i), ', ', num2str(y_i), ', ', num2str(z_eval), ')']);
