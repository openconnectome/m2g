% Fs = 1000; %frequency sample
% T = 1/Fs;
% L = 10000;
% t = (0:L) * T;
% x = .7*sin(2*pi*60*t) + .5*sin(2*pi*40*t);
% subplot(2,2,1)
% plot(Fs*t(1:60), x(1:60));
% title('x = .7*sin(2*pi*60*t) + .5*sin(2*pi*40*t)')
% xlabel('Time in ms')
% 
% NFFT = 2^nextpow2(L);
% X = fft(x, NFFT)/L;
% f = Fs/2 * linspace(0, 1, NFFT/2 + 1); % range of possible freq
% subplot(2,2,2)
% plot(f(1:NFFT/2 + 1), 2*abs(X(1:NFFT/2+1)));
% title('2*|X(w)|');
% xlabel('single sided frequencies');
% axis([0 100 0 1]);
% 
% n = 2*randn(size(t));
% y = x + n;
% subplot(2,2,3)
% plot(Fs*t(1:60), y(1:60));
% title('y = x with noise')
% xlabel('Time in ms')
% 
% Y = fft(y, NFFT)/L;
% subplot(2,2,4)
% plot(f(1:NFFT/2 + 1), 2*abs(Y(1:NFFT/2 + 1)));
% axis([0 100 0 1])
% title('2*|Y(w)|')
% xlabel('frequencies')
close all
clear all

Color = {'g', 'r', 'b'};
j = 1;
for i = [8, 10, 12]
    figure
    Fs = 1024;
    T = 1/Fs;
    L = 2^i;
    t  = ((0:L)*T)'; 
    x  = sin(2*pi*t*200) + sin(2*pi*120*t) + randn(size(t));
    Nx = length(x);
    % Window data
    w = hanning(Nx);
    xw = x.*w; 
    % Calculate power
    nfft = L; 
    X = fft(xw,nfft);
    mx = abs(X).^2; 
    % Normalize by window power and multiply by 2 to get one sided
    % spectrum...
    mx = mx/(w'*w); 
    NumUniquePts = nfft/2+1; 
    mx = mx(1:NumUniquePts);
    mx(2:end-1) = mx(2:end-1)*2;
    Pxx1 = mx/Fs;
    Fx1 = (0:NumUniquePts-1)*Fs/nfft; 
    [Pxx2,Fx2] = pwelch(x,w,0,nfft,Fs);
    plot(Fx1,10*log10(Pxx1), 'b*',Fx2,10*log10(Pxx2),'ro--');
    
    [Pxx3, f] = pmtm(x, 1.5, nfft, Fs);
    hold on
    plot(Fx1, 10*log10(Pxx3), 'g+--');
    legend('PSD via FFT','PSD via pwelch', 'PSD via PMTM');
    xlabel('Frequency');
    title(sprintf('Comparing different Power Spectrum Methods for L = %d', L));

end
