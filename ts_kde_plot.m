clear all;
d0 = load('/home/jliao2/Documents/data-set/livelab/sleep/a00-h.csv');
d1 = load('/home/jliao2/Documents/data-set/livelab/sleep/a01-h.csv');
d2 = load('/home/jliao2/Documents/data-set/livelab/sleep/b04-h.csv');
d3 = load('/home/jliao2/Documents/data-set/livelab/sleep/d04-h.csv');

% d0 = d0/sum(d0);
% d1 = d1/sum(d1);
% d2 = d2/sum(d2);
% d3 = d3/sum(d3);
d0 = d0/3600;
d1 = d1/3600;
d2 = d2/3600;
d3 = d3/3600;

figure(1);hold on;
plot(d0, '+b-');
plot(d1, '^r-');
plot(d2, 'ok-');
plot(d3, 'sg-');
grid on;
xlabel('time in a day (h)');
ylabel('histogram');