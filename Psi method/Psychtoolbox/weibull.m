function [psi,th] = weibull(theta,c,f)

th = CSF(theta,f); % threshold from CSF model
nAFC = 10; % number of forced choice (here 10)
w = 1/nAFC + (1-1/nAFC)*(1-exp(-2*(10^(th+log10(c)))));

lapse_rate = 0.04; % probability of human errors

psi = min(1-lapse_rate, w);

end