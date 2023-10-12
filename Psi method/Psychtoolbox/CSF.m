function qcsf = CSF(theta, f)

f_max = theta(1);       % peak frequency
gamma_max = theta(2);   % peak sensibility
beta = theta(3);        % FWHM (full width at half maximum)
delta = theta(4);       % truncation level in log units (decibel)

k = log10(2);
b = log10(2*beta);
qcsf = log10(gamma_max) - k*(2*(log10(f/f_max))/b).^2; % log-parabola

% truncation
if (f<f_max) && (qcsf<log10(gamma_max)-delta) 
    qcsf = log10(gamma_max)-delta;
end

qcsf(qcsf<0) = 0;

end