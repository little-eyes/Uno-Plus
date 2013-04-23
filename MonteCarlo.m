clear all;
GreedyResults = [];
MaxDeviceAvailability = [];
MeanDeviceAvailability = [];

for o = 1:10000
    nDevices = 20;
    nObjects = 100;
    nBudget = 10;
    nReplicas = [];
    DeviceAvailability = [];
    Budget = [];
    AccessFrequency = [];
    for i = 1:nObjects
        AccessFrequency = [AccessFrequency rand()];
    end
    for i = 1:nObjects
        nReplicas = [nReplicas nDevices*1.0/(1+exp(5*(0.5-AccessFrequency(i))))];
    end
    for i = 1:nDevices
        DeviceAvailability = [DeviceAvailability rand()];
        Budget = [Budget 0];
    end
    [SortedAccessFrequency, findex] = sort(AccessFrequency, 'descend');
    [SortedDeviceAvailability, dindex] = sort(DeviceAvailability, 'descend');
    ObjectAvailability = [];
    for i = 1:nObjects
        p = 1.0;
        r = 0;
        for k = 1:nDevices
            if Budget(dindex(k)) < nBudget
                Budget(dindex(k)) = Budget(dindex(k)) + 1;
                p = p * (1.0 - SortedDeviceAvailability(k));
                r = r + 1;
            end
            if r >= ceil(nReplicas(dindex(k)))
                break;
            end
        end
        ObjectAvailability = [ObjectAvailability 1.0-p];
    end
    GreedyResults = [GreedyResults SortedAccessFrequency*ObjectAvailability'];
    % calc the object func.
    s = [];
    for p = 1:nObjects
        s = [s (1-(1-max(DeviceAvailability))^ceil(nReplicas(findex(p))))];
    end
    MaxDeviceAvailability = [MaxDeviceAvailability sum(s.*AccessFrequency)];
end

%plot(GreedyResults, '.--b'); hold on;
%plot(MaxDeviceAvailability, '.--r');
plot(100*(MaxDeviceAvailability-GreedyResults)./MaxDeviceAvailability, '.');
hold on;
line([1;length(GreedyResults)], [100*min((MaxDeviceAvailability-GreedyResults)./MaxDeviceAvailability); 100*min((MaxDeviceAvailability-GreedyResults)./MaxDeviceAvailability)]);
min(GreedyResults./MaxDeviceAvailability)
max(GreedyResults./MaxDeviceAvailability)
hold off;
