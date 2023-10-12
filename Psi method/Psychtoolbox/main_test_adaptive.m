% Costraint: oberserver is at about 57 cm of distance from the screen
% @ 57 cm of distance, 1 cm ~ 1 deg of visual angle
% f max is 0.5 cpp ~ 22.6 cpd

clear; close all; clc;

%% PRE-TEST

load contrast2.mat
letter_code = 'cdhknorsvz';
%sf_code = [6/11.4, 12/11.4, 24/11.4, 48/11.4, 96/11.4];
%c_code = [0.0039, 0.0103, 0.0267, 0.0675, 0.1603];
np = size(letters,1);   % # pixels
nl = size(letters,3);   % # letters
nc = size(letters,4);   % # contrasts
nsf = size(letters,5);  % # spatial frequencies
nT = 50;                % # trials
nstim = nsf*nc;         % # stimuli
stimuli(1,:) = repmat(c_code,[1 nsf]);
stimuli(2,:) = repelem(sf_code,nc);

% 4D parameter space 
nval = 10;              % # parameter values
npar = 4;               % # parameters: f_max, gamma_max, beta, delta
nvec = nval^npar;       % # all possible parameter vectors 
nsam = 50;              % # samples
npick = nstim/10;
T_theta = zeros(nval,npar); 
t1=0.2; t2=20; t3=2; t4=2000; t5=1; t6=9; t7=0.02; t8=2; 
T_theta(:,1) = logspace(log10(t1),log10(t2),nval);     % f_max
T_theta(:,2) = logspace(log10(t3),log10(t4),nval);     % gamma_max
T_theta(:,3) = logspace(log10(t5),log10(t6),nval);     % beta
T_theta(:,4) = logspace(log10(t7),log10(t8),nval);     % delta
Param_space = zeros(nvec,npar);
Param_space(:,1) = repelem(T_theta(:,1),nval^(npar-1));
Param_space(:,2) = repmat(repelem(T_theta(:,2),nval^(npar-2)),nval^(npar-3),1);
Param_space(:,3) = repmat(repelem(T_theta(:,3),nval^(npar-3)),nval^(npar-2),1);
Param_space(:,4) = repmat(T_theta(:,4),nval^(npar-1),1);

% Probability density function
p_theta = ones(nval,npar)./(nval); 
prior = ones(1,nvec)./nvec;

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

% Output experiment
p.recLabel = {'trial' 'contrast' 'spatial frequency' 'respCorrect'};
rec = zeros(nT, length(p.recLabel));
rec(:,1) = 1:nT;

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

%% qCSF TEST

for t=1:nT

    % Sampling 4d param space
    ind_sample =  discretesample(prior,nsam);
    theta_sampled = Param_space(ind_sample,:);

    % Computing information gain (for each stimulus)
    prob_stim_single_theta = zeros(nsam,nstim);
    for st = 1:nstim
        con = stimuli(1,st);
        sfreq = stimuli(2,st);
        for s = 1:nsam
            prob_stim_single_theta(s,st) = weibull(theta_sampled(s,:),con,sfreq);
        end
        sum_prob_stim_all_theta = sum(prob_stim_single_theta)/nsam;
    end

    information_gain = -sum_prob_stim_all_theta.*log(sum_prob_stim_all_theta)-(1-sum_prob_stim_all_theta).*log(1-sum_prob_stim_all_theta)-sum_prob_stim_all_theta;
    [~, ind_stimuli] = sort(information_gain,'descend');
    random_pick = randi(npick);
    ind_stimuli = ind_stimuli(1:npick);
    ind_next_stim = ind_stimuli(random_pick);
    tmp = rem(ind_next_stim,nc);
    tmp(tmp==0) = 6;
    rec(t,2) = tmp;
    rec(t,3) = floor(ind_next_stim/nc);

    % Completion % + all possible output (###)
    tmp = round(100*(t-1)/nT,1)+"%";
    string = [convertStringsToChars(tmp) ' - ' upper(letter_code)];

    % Show stimulus
    Snd('Play',sound_on);
    a = randi(nl);

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
            rec(t,4) = letter_code(a)==keyCode; % correctness
            kb_waiting=0; 
        end
    end

    prob_stim_correctness = zeros(1,nvec);

    for i=1:nvec
        tmp = weibull(Param_space(i,:), stimuli(1,ind_next_stim), stimuli(2,ind_next_stim));
        if ~rec(t,4)
            tmp = 1-tmp;
        end
        prob_stim_correctness(i) = tmp;
    end
    response_rate = sum(prob_stim_correctness.*prior);
    posterior = prior.*prob_stim_correctness/response_rate;
    prior = posterior;
end

% Find max param

p_theta_post = zeros(nval,npar);

for i=1:nval
    p_theta_post(i,1) = sum(posterior((i-1)*nval^3+1:(i-1)*nval^3+nval^3));
end

for i=1:nval
    x2 = 0;
    for j=1:nval
        x2 = x2 + sum(posterior( (j-1)*nval^3+(i-1)*nval^2+1 : (j-1)*nval^3+(i-1)*nval^2+nval^2 ));
    end
    p_theta_post(i,2) = x2;
end

for i=1:nval
    x3 = 0;
    for j=1:nval^2
        x3 = x3 + sum(posterior( (j-1)*nval^2+(i-1)*nval+1 : (j-1)*nval^2+(i-1)*nval+nval ));
    end
    p_theta_post(i,3) = x3;
end

v4=1:nvec;
for i=1:nval
    x41 = rem(v4,nval)==i-1;
    x42 = find(x41==1);
    x43 = sum(posterior(x42));
    p_theta_post(i,4) = x43;
end

a = find(p_theta_post==max(p_theta_post));
theta = T_theta(a);

save registrazioni\federico2.mat rec p posterior theta

sca;