% script for computing TRT using the Hellenger Distance
%function body
% loads the .mat files containing all the timeseries information for 
% all of the subjects 
% computes fft of each timeseries
% uses the ft to compute the power per frequency band on the timeseries
% from the power per freqneucy band, compute the kernel density estimate
% use the KDE to compute hellenger distance between all pairs
% plot TRT

% copyright 2015
% written by Eric Bridgeford on 2015-05-18

filenames = fopen('Datasets\kkisubnames.txt');
base = 'Datasets\KKI_data\';
Mtx = zeros(42, 70, 210);
i = 1;
val = fgets(filenames);
while (ischar(val))
   stru = load(base + val);
   Mtx[i,:,:] = stru.roi_data;
   i = i + 1;
   val = fgets(filenames);
end