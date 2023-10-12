clear; close all; clc;

letter_code='CDHKNORSVZ';
nL = length(letter_code);   % number of letters
nP = 512;                   % number pixels
nSF = 9;                    % number of sptail frequencies
letter_image = zeros(nP,nP,nL);
fourier_image = zeros(nP,nP,nL);
letter_filtered = zeros(nP,nP,nL,nSF); % each letter is filtered for nSF different spatial frequencies

for_python = 1;   % =1 if you want to export on python (psychopy)

for l=1:nL

    % Creating letter images
    filename = "letter\letter-"+upper(letter_code(l))+"-256.jpg";
    tmp = imread(filename);
    tmp = rgb2gray(tmp);        % from rgb to gray scale
    tmp = imbinarize(tmp);
    tmp = imcomplement(tmp);    % letter white, background black
    letter_image(nP/4+1:3*nP/4,nP/4+1:3*nP/4,l)=tmp; % image centered in new image (512x512)

    %figure
    %subplot(2,5,1)
    %imagesc(letter_image(:,:,l))
    %colormap('gray')

    fourier_image(:,:,l) = fftshift(fft2(letter_image(:,:,l))); % fourier transform of the new images

    % Filter design

    x = psdfreqvec('npts',512,'Fs',1);
    select = 1:256;
    x = fftshift([x(select); x(select(end)+1:end)-1]);
    [x,y] = meshgrid(x); % create meshgrid coordinates in frequency domain
    f = sqrt(x.^2 + y.^2); % radial distance in frequency space

    % Filtering images

    sf_code = logspace(-1,2,nSF); % cycles/degree (at 57cm, cm=degree)
    f_peak = sf_code*50.8/1920;   % from cycles/degree to cycles/pixel (display settings)
    
    for sf = 1:numel(f_peak)
        f0 = f_peak(sf);
        filter = 1/2 + cos(pi* (log(f/f0)) / (log(2)))/2; % raised cosine log filter
        filter(f<f0/2 | f>2*f0)=0;
        
        h = ifft2(fftshift(fourier_image(:,:,l).*filter));
   
        % Psychopy
        if for_python   
            h(h<0)=h(h<0)/abs(min(h(:)));
            h(h>0)=h(h>0)/abs(max(h(:)));
%             h1 = h-(max(h(:))+min(h(:)))/2;     % centered to 0
%             h2 = h1/max(h1(:));                 % -1<val<1
            letter_filtered(:,:,l,sf) = h;
            subplot(2,5,sf+1)
            imagesc(h)
            colormap('gray')

        % Psychtoolbox
        else            
            ha = h*255/((max(h(:))-min(h(:))));   % range 255
            hb = ha-min(ha(:));                   % 0<val<255
            letter_filtered(:,:,l,sf) = hb;
            subplot(2,5,sf+1)
            imagesc(hb)
            colormap('gray')
        end

    end

end

% save letter_python.mat letter_filtered sf_code