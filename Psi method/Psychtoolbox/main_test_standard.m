% Costraint: oberserver is at about 57 cm of distance from the screen
% at 57 cm of distance, 1 cm ~ 1 deg of visual angle 

clear; close all; clc;

load contrast2.mat
letter_code = 'cdhknorsvz';
sf_code = [6/11.4, 12/11.4, 24/11.4, 48/11.4, 96/11.4];
c_code = [0.0039, 0.0103, 0.0267, 0.0675, 0.1603];
np = size(letters,1);   % # pixels
nl = size(letters,3);   % # letters
nc = size(letters,4);   % # contrasts
nsf = size(letters,5);  % # spatial frequencies
nr = 20;                % # repeats (for each contrast and spatial frequency)
nT = nr*nc*nsf;         % # trials

% Psychtoolbox settings
Screen('Preference', 'SkipSyncTests', 1);
Screen('Preference', 'TextRenderer', 0);
PsychDefaultSetup(2);
myscreen = 2; % which monitor is used (o both, 1 own, 2 ext)

% Screen settings
[win,screen_dim] = Screen('OpenWindow',myscreen,[127 127 127]);
[width, height] = Screen('DisplaySize', myscreen);
width = width/10;                  % cm
height = height/10;                % cm
p.ppd = screen_dim(3)/width;       % pixels per deg (1cm = 1deg at 57 cm distance)
p.sf = sf_code/p.ppd;              % compute spatial frequency in cycles per pixel
Priority(MaxPriority(win));

% Create fixation dot and sound effects
fixRect = CenterRect([0 0 8 8], screen_dim); % 8x8 pixel fixation dot
sound_on = MakeBeep(400,.1); % freq,dur
sound_off = MakeBeep(200,.1); % freq,dur
stimDur=0.1; % in seconds

% Output experiment (shuffling c and sf values)
p.recLabel = {'trial' 'cIndex' 'sfIndex' 'correctLetter' 'response' 'respCorrect'};
rec = zeros(nT, length(p.recLabel));
rec(:,1) = 1:nT;
cIndex = repmat(1:nc, [nsf 1 nr]);
sfIndex = repmat(1:nsf, [1 nc nr]);
[rec(:,2), ind] = Shuffle(cIndex(:));
[rec(:,3)] = sfIndex(ind);

% Show intro
intro1 = 'Press letter corresponding to the stimulus';
intro2 = 'Turn CAPS LOCK off';
intro3 = 'Press space bar to start the experiment';
Screen('TextSize', win, 30);   
Screen('DrawText',win,intro1,screen_dim(3)/2-length(intro1)*11.25,3*screen_dim(4)/8);
Screen('DrawText',win,intro2,screen_dim(3)/2-length(intro2)*11.25,screen_dim(4)/2);
Screen('DrawText',win,intro3,screen_dim(3)/2-length(intro3)*11.25,5*screen_dim(4)/8);
Screen('Flip', win);
kb_waiting = 1;
while kb_waiting
    KbWait;
    [~,~,k] = KbCheck;
    keyCode = KbName(k);
    if strcmp(keyCode, 'space')
        kb_waiting=0; 
    end
end
Screen('FillOval', win, 0, fixRect);
Screen('Flip',win);
WaitSecs(stimDur);
Screen('TextSize',win,50);

for t=1:nT

    % Completion % + all possible output (###)
    tmp = round(100*(t-1)/nT,1)+"%";
    string = [convertStringsToChars(tmp) ' - ' upper(letter_code)];

    % Show stimulus
    Snd('Play',sound_on);
    a = randi(nl);
    rec(t,4) = letter_code(a);
    im = letters(:,:,a,rec(t,2),rec(t,3));
    l = Screen('MakeTexture',win,im);
    m = mean(mean(im));
    Screen('FillRect',win,[m m m]);
    Screen('DrawTexture', win, l); % stimulus
    Screen('DrawText',win,string,10,10,[0 0 0]); % (###)
    Screen('Flip',win);
    WaitSecs(stimDur);
    Snd('Play',sound_off);

    % Show (###) and fixation dot while waiting answer
    Screen('DrawText',win,string,10,10,[0 0 0]);
    Screen('FillOval', win, 0, fixRect);
    Screen('Flip',win);
    
    % Record answer (only ESC or possible output, i.e. 10 letters)
    kb_waiting = 1;
    while kb_waiting
            KbWait;
            [~,~,k] = KbCheck;
            keyCode = KbName(k);
        if strcmp(keyCode, 'ESCAPE')
            sca
            break; % to quit experiment
        elseif strcmp(keyCode, 'c') || strcmp(keyCode, 'd') || strcmp(keyCode, 'h')...
                || strcmp(keyCode, 'k') || strcmp(keyCode, 'n') || strcmp(keyCode, 'o')...
                || strcmp(keyCode, 'r') || strcmp(keyCode, 's') || strcmp(keyCode, 'v')...
                || strcmp(keyCode, 'z')
            rec(t,5) = keyCode;
            rec(t,6) = rec(t,4)==rec(t,5);
            kb_waiting=0; 
        end
    end
end

% save exp.mat rec p

sca;