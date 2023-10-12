x = linspace(0,1,100);
y1 = -x.*log2(x) - (1-x).*log2(1-x);
y2 = -x.*log(x) - (1-x).*log(1-x);

plot(x,y1)
hold on
plot(x,y2)

rap= y2./y1;