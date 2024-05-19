function [per_15min_min_connected_evs_single_day, per_15min_max_connected_evs_single_day, per_15min_mean_connected_evs_single_day] = computeSecondDayPredictionProfileOfNoEVsPer15Minutes(per_second_connected_evs_single_day)
    % for every 15 minute, now compute the min, max, and average number of connected EVs
    interval = 15*60; % 900
    per_15min_min_connected_evs_single_day = [];
    per_15min_max_connected_evs_single_day = [];
    per_15min_mean_connected_evs_single_day = [];
    slots = 86400 / interval; % 96

    for x = 0:slots - 1
        list_values = [];
        for y = 1:interval
            list_values = [list_values per_second_connected_evs_single_day(x * interval + y)];
        end
        
        per_15min_min_connected_evs_single_day = [per_15min_min_connected_evs_single_day; min(list_values)];
        per_15min_max_connected_evs_single_day = [per_15min_max_connected_evs_single_day; max(list_values)];
        per_15min_mean_connected_evs_single_day = [per_15min_mean_connected_evs_single_day; mean(list_values)];
    end
        
end