clear; close all; clc;
set(0,'DefaultFigureColormap',feval('gray'));

letter_code='CDHKNORSVZ';
n = length(letter_code);        % number of letters
p = 512;                        % number of pixels
letter_image = zeros(p,p,n);
fourier_image = zeros(p,p,n);
letter_filtered = zeros(p,p,n);

for_python = 1;   % =1 if you want to export on python (psychopy)

for l=1:n   % for each letter

% Creating letter images

    filename = "letter\letter-"+upper(letter_code(l))+"-256.jpg";
    tmp = imread(filename);
    tmp = rgb2gray(tmp);        % from rgb to gray scale
    tmp = imbinarize(tmp);
    tmp = imcomplement(tmp);    % letter white, background black
    letter_image(p/4+1:3*p/4,p/4+1:3*p/4,l)=tmp;    % image centered in new image (512x512)

    fourier_image(:,:,l) = fftshift(fft2(letter_image(:,:,l))); % fourier transform of the new images

% Filter design

    x=psdfreqvec('npts',512,'Fs',1);
    select = 1:256;
    x = fftshift([x(select); x(select(end)+1:end)-1]);
    [x,y] = meshgrid(x); % create meshgrid coordinates in frequency domain
    f = sqrt(x.^2 + y.^2); % radial distance in frequency space

    f0 = 3/256;
    filter = 1/2 + cos(pi* (log(f/f0)) / (log(2))) /2;
    filter(f<f0/2 | f>2*f0)=0;

% Filtering images
    h = ifft2(fftshift(fourier_image(:,:,l).*filter));
    
    if for_python
        h1 = h-(max(max(h))+min(min(h)))/2;     % centered to 0
        h2 = h1/max(max(h1));                   % -1<val<1
        letter_filtered(:,:,l) = h2;
    else
        ha = h*255/((max(max(h))-min(min(h)))); % range 255
        hb = ha-min(min(ha));                   % 0<val<255
        letter_filtered(:,:,l) = hb;
    end

    figure
    imagesc(letter_filtered(:,:,l))
end

% save letters.mat letter_filtered