Fs = 1000; %frequency sample
T = 1/Fs;
L = 10000;
t = (0:L) * T;
x = .7*sin(2*pi*60*t) + .5*sin(2*pi*40*t);
subplot(2,2,1)
plot(Fs*t(1:60), x(1:60));
title('x = .7*sin(2*pi*60*t) + .5*sin(2*pi*40*t)')
xlabel('Time in ms')

NFFT = 2^nextpow2(L);
X = fft(x, NFFT)/L;
f = Fs/2 * linspace(0, 1, NFFT/2 + 1); % range of possible freq
subplot(2,2,2)
plot(f(1:NFFT/2 + 1), 2*abs(X(1:NFFT/2+1)));
title('2*|X(w)|');
xlabel('single sided frequencies');
axis([0 100 0 1]);

n = 2*randn(size(t));
y = x + n;
subplot(2,2,3)
plot(Fs*t(1:60), y(1:60));
title('y = x with noise')
xlabel('Time in ms')

Y = fft(y, NFFT)/L;
subplot(2,2,4)
plot(f(1:NFFT/2 + 1), 2*abs(Y(1:NFFT/2 + 1)));
axis([0 100 0 1])
title('2*|Y(w)|')
xlabel('frequencies')
