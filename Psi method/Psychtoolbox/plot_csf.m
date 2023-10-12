clear; close all; clc;

% loading results from experiments (ex. main_test_adaptive.m))
% theta -> estimated param of qCSF

%load registrazioni\random1.mat

n = 1000;
freq = logspace(log10(0.2),log10(100),n);
con = logspace(-3,0,n);
weib = zeros(n);
th = zeros(1,n);

for f=1:n
    for c=1:n
        [weib(c,f),th(f)] = weibull(theta,freq(f),con(c));
    end
end

% figure
% subplot(1,2,1)
% loglog(freq,th,'LineWidth',2)
% title('quick Contrast Sensitivity Function (qCSF)')
% xlabel('Spatial Frequency')
% ylabel('Contrast Sensitivity (1/c)')
% subplot(1,2,2)
% ft = 50;
% semilogx(con,weib(:,ft),'LineWidth',2,'Color','r')
% title("Psychometric Function (Weibull Distribution), spatial frequency f=" + freq(ft) + " cpd")
% xlabel('Contrast Level')
% ylabel('% Correct Answer')

figure
imagesc(weib) % probability stimulus correctly seen
ax = gca;
ind_tick = [1,4,7,10]*n/10;
ax.XTick = ind_tick;
ax.YTick = ind_tick;
ax.XTickLabel = freq(ind_tick);
ax.YTickLabel = con(ind_tick).*100;
title('qCSF 2D Probability Distribution')
xlabel('Spatial Frequency')
ylabel('Contrast Sensitivity (1/c)')
colormap('jet')
h = colorbar;
ylabel(h, '% Correct Answer')
hold on
a1 = zeros(1,n);
for i=1:n
    a1(i) = find(weib(:,i)>=0.8782,1,'first'); % threshold in weibull function
end
plot(a1,'LineWidth',2) % qCSF values (thresholds)

% hold on
% line([ft, ft], [1, n], 'Color','r','LineWidth',2)
% legend({'Threshold qCSF (sx)','Weibull Distribution (dx)'})
