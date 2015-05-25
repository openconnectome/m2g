%% playing around with correlations

%% One Variable; two conditions

k = 10000; % choose a sample size
N = randn(k, 1); % create a population of the sample size from a gaussian distribution
                    % with mean 0 and sd 1
                    
n = [8 64 512];  % choose different sample sizes

for i = 1:length(n)
    sa = []; sb = [];
    % use randsample to draw samples of size n(i)
    sa = randsample(N, n(i));
    sb = randsample(N, n(i));
    
    % compute the average of the differences between the means of the
    % samples
    
    d_empir(i) = mean(sa) - mean(sb); % expect a value of 0 for the whole population
end

color = {'b', 'r', 'g', 'k'};
figure
hold on
for j = 1:length(n)
   sa = zeros(k, n(j));
   sb = sa;
   for i = 1:k
       sa(i, :) = randsample(N, n(j));
       sb(i, :) = randsample(N, n(j));
   end
   
   d = mean(sa,2) - mean(sb,2);  % compute the distribution of differences between the means 
                                 % sample pairs
                                 
    % make a histogram of the distribution of the differences
    % scale the distributions to transform to probabilities

    [nn, xx] = hist(d, 20);
    bar(xx, nn/sum(nn), color{j});
  
end


% formatting the graph
title(sprintf('Probability of getting a difference between\n two random samples of a given sample size.'));
ylabel('Probability of occurance');
xlabel('Difference between the two samples');
legend('sample size = 8', 'sample size = 64', 'sample size = 512');

for i = 1:length(n)
    plot([d_empir(i), d_empir(i)],[0 .2],'-', 'Color', color{i}, 'LineWidth',2);
end

%% bootstrap to generate equivalent of a T-test
%use a chi-square distribution with 6 degrees of freedom and gaussian dist
% centered at 0 and std of 1

k = 10000;
N = [random('chisquare', 6, [k/2, 1]); random('norm', 0, 1, [k/2, 1])];

% compute mean, median, and std for the populations

meaN = mean(N);
medN = median(N);
stdN = std(N);

% look at the population

figure;
hist(N, 100);
hold on
y = get(gca, 'yLim');

plot([meaN, meaN], y*.99, 'r-');
plot([medN, medN], y*.99, 'g-');
plot([meaN - stdN, meaN + stdN], [y(2)*.5, y(2)*.5], 'r-');
title('Simulated Distribution')

