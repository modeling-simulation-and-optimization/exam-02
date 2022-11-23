%{
    Exam 2
    Exercise 2

    Made by:
    Juan Andrés Romero C - 202013449
    Juan Sebastián Alegría - 202011282
%}

clc, clear all, close all;

syms f_x x;

f_x = x.^5 - 8 * x.^3 + 10 * x + 6;

figure
ezplot(f_x)
xlim([-3 3])
ylim([-10 25])
hold on;

d1_f_x = diff(f_x); % First derivative of f_x
d2_f_x = diff(d1_f_x); % Second derivative of f_x

x_limit = 2.5; % Stop point for the calculations
x_ini = -2.5; % Starting value for x

local_limits_x = [];
local_limits_y = [];

while x_ini < x_limit
    d1_f_x_i = double(subs(d1_f_x, x, x_ini));

    convergence = 0.001; % Convergence value

    alpha = 0.1;

    while abs(d1_f_x_i) > convergence

        d1_f_x_i = double(subs(d1_f_x, x_ini)); % First derivative evaluated in the starting value

        d2_f_x_i = double(subs(d2_f_x, x_ini)); % Second derivative evaluated in the starting value

        x_found = x_ini - alpha * (d1_f_x_i / d2_f_x_i); % Newton-Raphson equation: x(i+1) = x(i) - alpha*f'(x(i))/f''(x(i))

        x_ini = x_found; % Updating the x value for the next iteration

        f_x_i = double(subs(f_x, x_ini)); % Evaluating the x value in f_x in order to plot the value found

        plot(x_ini, f_x_i, 'or'); % Plotting the found value
    end

    local_limits_x = [local_limits_x; x_ini]; % Storing the x limit value found in an array
    local_limits_y = [local_limits_y; f_x_i]; % Storing the y limit value found in an array
    x_ini = x_ini + 1; % Updating the starting value for x to find the next limit
end

% Finding the coordinates of the global max and global min
global_max_y = max(local_limits_y);
global_min_y = min(local_limits_y);

global_max_x = local_limits_x(find(local_limits_y == global_max_y));
global_min_x = local_limits_x(find(local_limits_y == global_min_y));

% Plotting
text(global_max_x - 0.2, global_max_y + 2, ['Global Max: (', num2str(global_max_x), ', ', num2str(global_max_y), ')']);
text(global_min_x - 1.75, global_min_y - 2, ['Global Min: (', num2str(global_min_x), ', ', num2str(global_min_y), ')']);
