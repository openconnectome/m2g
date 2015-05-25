clear all
close all

files = dir('*.mat');
c = 1;
for i = 1:76
    temp = files(i).name;
    mtx = load(temp); % log10
    tgraph = mtx.roi_data;
    tgraph(isinf(tgraph))=0;
    %     tgraph=full(temp.graph);
    smg(:,:,c) = tgraph;
    
    c = c+1;
end

% compute the pairwise correlation for sake of comparison
for i = 1:76
    pair(i,:,:) = corr(smg(:,:,i)');
end

for i = 1:76
    for j = 1:76
        gErr(i,j) = sum(sum((pair(i,:,:) - pair(j,:,:)).^2));
    end
end

%% Compute TRT
figure(2), imagesc(log(gErr)), colorbar
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