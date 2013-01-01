clear all;
a01 = load('a01.csv');
a02 = load('a02.csv');
a03 = load('a03.csv');
a04 = load('a04.csv');
a05 = load('a05.csv');
a06 = load('a06.csv');
a07 = load('a07.csv');
a08 = load('a08.csv');
a09 = load('a09.csv');
a10 = load('a10.csv');
a11 = load('a11.csv');
b02 = load('b02.csv');
b03 = load('b03.csv');
b04 = load('b04.csv');
b05 = load('b05.csv');
b06 = load('b06.csv');
b07 = load('b07.csv');
b08 = load('b08.csv');
b09 = load('b09.csv');
b10 = load('b10.csv');
b11 = load('b11.csv');
mx = [max(a01), max(a02), max(a03), max(a04), max(a05), max(a06), max(a07), max(a08), max(a09), max(a10), max(a11), max(b02), max(b03), max(b04), max(b05), max(b06), max(b07), max(b08), max(b09), max(b10), max(b11)];
mi = [min(a01), min(a02), min(a03), min(a04), min(a05), min(a06), min(a07), min(a08), min(a09), min(a10), min(a11), min(b02), min(b03), min(b04), min(b05), min(b06), min(b07), min(b08), min(b09), min(b10), min(b11)];
me = [mean(a01), mean(a02), mean(a03), mean(a04), mean(a05), mean(a06), mean(a07), mean(a08), mean(a09), mean(a10), mean(a11), mean(b02), mean(b03), mean(b04), mean(b05), mean(b06), mean(b07), mean(b08), mean(b09), mean(b10), mean(b11)];
x = [mx; me; mi];
y = sortrows(x')';

mean_replica = mean(me)
var_replica = std(me)

balance = load('balance.csv');
while length(balance) < 21
    balance = [balance; 0];
end
mean_balance = mean(balance)
var_balance = std(balance)
storage = load('storage.csv');
mean_storage = mean(storage)
var_storage = std(storage)

ar = load('success.csv');
mean_ar = mean(ar)
var_ar = std(ar)

% figure(2); hold on;
% for i = 1:21
%    plot([i i], [y(1,i) y(3,i)], 'ks-', 'linewidth', 2, 'markersize', 3);
% end
% plot([1:21], y(2,:), 'k:', 'linewidth', 2.5)
% axis([0 22 0 12]);
% grid on;
% hold off;
% 
% figure(3); hold on;
% boxplot(y);