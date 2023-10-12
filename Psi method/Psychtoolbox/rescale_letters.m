clear; close all; clc;

%load prove/letters.mat

np = size(letter_filtered,1);   % number pixels
nl = size(letter_filtered,3);   % number letters
nc = 6;                         % number contrast values
nsf = 5;                        % number spatial frequencies
c_code = logspace(log10(1), log10(128), nc);
sf_code = [1 1/2 1/4 1/8 1/16]; % rescale values (real SF depends on distance from monitor)

letters = zeros(np,np,nl,nc,nsf); 

for l = 1:nl
      % figure
    for c = 1:nc
        im = letter_filtered(:,:,l);
        im2 = (im - mean(mean(im)))*c_code(c)+127; % mean to 127, rescaled by contrast values in c_code
%         subplot(2,3,c)
%         imagesc(im2)
%         colormap('gray')
%         caxis([0 255]);

        for f = 1:nsf
            im3 = imresize(im2,sf_code(f)); % rescale letters (downsampling)
            a = size(im3,1);
            d = (np-a)/2; % calculate limit value in the new image
            im4 = zeros(np,np) + mean(mean(im3)); % background set as the mean value
            im4(d+1:a+d,d+1:a+d) = im3; % centered on the new image (512x512 in each case)
            letters(:,:,l,c,f) = im4;

            %subplot(nc,nsf,nsf*(c-1)+f)
            %imagesc(im4)
            %colormap('gray')
            %caxis([0 255]);
        end

    end

end

%save contrast2.mat letters sf_code c_code