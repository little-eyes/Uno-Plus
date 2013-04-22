clear all;

balance = load('balance.csv');
while length(balance) < 21
    balance = [balance; 0];
end
%mean_balance = mean(balance)
var_balance = std(balance)/max(balance)
storage = load('storage.csv');
%mean_storage = mean(storage)
var_storage = std(storage)/max(storage)

%ar = load('success.csv');
%mean_ar = mean(ar)
%var_ar = std(ar)

% figure(1);
% bar(sort(balance, 'descend'));
% %plot(sort(balance, 'descend'), '-s', 'linewidth', 2);
% set(gca, 'fontsize', 14);
% xlabel('device');
% ylabel('requests');
% axis([0 22 0 8000]);
% grid on;
% 
% figure(2);
% bar(sort(storage, 'descend'));
% %plot(sort(storage, 'descend'), '-s', 'linewidth', 2);
% set(gca, 'fontsize', 14);
% xlabel('device');
% ylabel('storage cost');
% axis([0 22 0 160]);
% grid on;

% a01 = load('a01_replica.csv');
% a02 = load('a02_replica.csv');
% a03 = load('a03_replica.csv');
% a04 = load('a04_replica.csv');
% a05 = load('a05_replica.csv');
% a06 = load('a06_replica.csv');
% a07 = load('a07_replica.csv');
% a08 = load('a08_replica.csv');
% a09 = load('a09_replica.csv');
% a10 = load('a10_replica.csv');
% a11 = load('a11_replica.csv');
% b02 = load('b02_replica.csv');
% b03 = load('b03_replica.csv');
% b04 = load('b04_replica.csv');
% b05 = load('b05_replica.csv');
% b06 = load('b06_replica.csv');
% b07 = load('b07_replica.csv');
% b08 = load('b08_replica.csv');
% b09 = load('b09_replica.csv');
% b10 = load('b10_replica.csv');
% b11 = load('b11_replica.csv');
% 
% data = [];
% N = max([length(a01), length(a02), length(a03), length(a04), length(a05), length(a06), length(a07), length(a08), length(a09), length(a10), length(a11), length(b02), length(b03), length(b04), length(b05), length(b06), length(b07), length(b08), length(b09), length(b10), length(b11)]);
% data = [data; [a01' NaN(1, N-length(a01))+1]];
% data = [data; [a02' NaN(1, N-length(a02))+1]];
% data = [data; [a03' NaN(1, N-length(a03))+1]];
% data = [data; [a04' NaN(1, N-length(a04))+1]];
% data = [data; [a05' NaN(1, N-length(a05))+1]];
% data = [data; [a06' NaN(1, N-length(a06))+1]];
% data = [data; [a07' NaN(1, N-length(a07))+1]];
% data = [data; [a08' NaN(1, N-length(a08))+1]];
% data = [data; [a09' NaN(1, N-length(a09))+1]];
% data = [data; [a10' NaN(1, N-length(a10))+1]];
% data = [data; [a11' NaN(1, N-length(a11))+1]];
% data = [data; [b02' NaN(1, N-length(b02))+1]];
% data = [data; [b03' NaN(1, N-length(b03))+1]];
% data = [data; [b04' NaN(1, N-length(b04))+1]];
% data = [data; [b05' NaN(1, N-length(b05))+1]];
% data = [data; [b06' NaN(1, N-length(b06))+1]];
% data = [data; [b07' NaN(1, N-length(b07))+1]];
% data = [data; [b08' NaN(1, N-length(b08))+1]];
% data = [data; [b09' NaN(1, N-length(b09))+1]];
% data = [data; [b10' NaN(1, N-length(b10))+1]];
% data = [data; [b11' NaN(1, N-length(b11))+1]];
% 
% 
% mx = [max(a01), max(a02), max(a03), max(a04), max(a05), max(a06), max(a07), max(a08), max(a09), max(a10), max(a11), max(b02), max(b03), max(b04), max(b05), max(b06), max(b07), max(b08), max(b09), max(b10), max(b11)];
% mi = [min(a01), min(a02), min(a03), min(a04), min(a05), min(a06), min(a07), min(a08), min(a09), min(a10), min(a11), min(b02), min(b03), min(b04), min(b05), min(b06), min(b07), min(b08), min(b09), min(b10), min(b11)];
% me = [mean(a01), mean(a02), mean(a03), mean(a04), mean(a05), mean(a06), mean(a07), mean(a08), mean(a09), mean(a10), mean(a11), mean(b02), mean(b03), mean(b04), mean(b05), mean(b06), mean(b07), mean(b08), mean(b09), mean(b10), mean(b11)];
% mean(me)
% %x = sortrows([mi; me; mx]');
% %x = x';
% figure(3);
% boxplot(data');
% grid on;
% set(gca, 'fontsize', 14);
% xlabel('devices');
% ylabel('replication factor');
% axis([1 21 0 15]);

t = [100 200 300 400 500 600 700 800 900 1000];
%l = [27.11 25.10 25.28 24.78 23.36 23.05 24.70 27.07 25.59 26.11];
%s = [16.19 26.81 40.40 44.15 34.50 29.01 29.20 29.38 29.37 29.36];
l = [3.84 30.51 23.20 26.24 27.90 23.91 21.55 25.24 23.74 21.30];
s = [13.61 25.13 29.98 34.64 38.59 40.38 42.63 42.42 44.05 41.16];
plot(t, l, '-bs', 'linewidth', 2);
hold on;
plot(t, s, '-ro', 'linewidth', 2);
set(gca, 'fontsize', 14);
xlabel('Storage Budget');
ylabel('Variance (%)');
legend('Load Balance', 'Storage Balance');
grid on;