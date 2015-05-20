files = dir('*.mat');

c = 1;
for i = 1:38
    temp = files(i).name;
    mtx = load(temp); % log10
    tgraph = mtx.roi_data;
    tgraph(isinf(tgraph))=0;
    %     tgraph=full(temp.graph);
    smg(:,:,c) = tgraph;
    
    c = c+1;
end

% compute the transform of each to obtain frequency spectrum
L = 210; % length of the time signal
NFFT = 2^nextpow2(L); 
Fs = 1;
T = 1/Fs;
t = (0:L-1)*T;
for c = 1:38
    for i = 1:70
        ftgra(i,:,c) = fft(smg(i,:,c), NFFT)/L; % fourier transform of the timeseries
        pwr(i,:,c) = abs(ftgra(i,:,c)).^2;
        pwr(i,:,c) = pwr(i,:,c)/sum(pwr(i,:,c));    
        kdens(i,:,c) = ksdensity(pwr(i,:,c));
    end
end

%use the kernel density to compute the hellenger distance between each
%pair of scans
for j = 1:70
    for a = 1:38
        for b = 1:38
            %j is the roi number, i is the scan, z is the scan being compared
            %to
            H(j,a,b) = norm(kdens(j,:,a) - kdens(j,:,b))/sqrt(2);
    
        end
    end
end
numrois = 70;
for i = 1:38
    for j = 1:38
        gErr(i,j) = (1/numrois)*sum(H(:,i,j));
    end
end

%% Compute TRT
figure(1), imagesc(log(gErr)), colorbar
matches = 0;
intra = 0; inter = 0;
intravec = [];
intervec = [];
for i = 1:1:size(gErr,1)
    temp = sort(gErr(i,:));
    q = i-1+2*mod(i,2);
    matches = matches + (temp(2)==gErr(i,q));
    intra = intra + gErr(i,q);
    temp2 = sum([gErr(i,1:q-1), gErr(i,q+1:end)])/40; %40 bc 1 is intra, 1 is me
    inter = inter + temp2;
    intravec = [intravec, gErr(i,q)];
    if i < q
        if i > 1
            intervec = [intervec, gErr(i,q-2), gErr(i,q+1:end)];
        else
            intervec = [intervec, gErr(i,q+1:end)];
        end
    else
        if i > 2
            intervec = [intervec, gErr(i,q-1), gErr(i,q+2:end)];
        else
            intervec = [intervec, gErr(i,q+2:end)];
        end
    end
end
intra = intra/42;
inter = inter/42;
title(strcat('correct matches=', num2str(matches),'/', num2str(size(smg,3))));

% compute the pairwise correlation for sake of comparison
for i = 1:38
    pair(i,:,:) = corr(smg(:,:,i)');
end

for i = 1:38
    for j = 1:38
        gErr(i,j) = sum(sum((pair(i,:,:) - pair(j,:,:)).^2));
    end
end

%% Compute TRT
figure(2), imagesc(log(gErr)), colorbar
set(gca, 'yscale','log')
matches = 0;
intra = 0; inter = 0;
intravec = [];
intervec = [];
for i = 1:1:size(gErr,1)
    temp = sort(gErr(i,:));
    q = i-1+2*mod(i,2);
    matches = matches + (temp(2)==gErr(i,q));
    intra = intra + gErr(i,q);
    temp2 = sum([gErr(i,1:q-1), gErr(i,q+1:end)])/40; %40 bc 1 is intra, 1 is me
    inter = inter + temp2;
    intravec = [intravec, gErr(i,q)];
    if i < q
        if i > 1
            intervec = [intervec, gErr(i,q-2), gErr(i,q+1:end)];
        else
            intervec = [intervec, gErr(i,q+1:end)];
        end
    else
        if i > 2
            intervec = [intervec, gErr(i,q-1), gErr(i,q+2:end)];
        else
            intervec = [intervec, gErr(i,q+2:end)];
        end
    end
end
intra = intra/42;
inter = inter/42;
title(strcat('correct matches=', num2str(matches),'/', num2str(size(smg,3))));