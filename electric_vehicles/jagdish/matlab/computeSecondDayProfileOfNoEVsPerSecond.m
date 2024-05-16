function per_second_connected_evs_single_day = computeSecondDayProfileOfNoEVsPerSecond(sorted_stored_values)
    current_ts = 1;
    %[nr nc] = size(sorted_stored_values);
    
    per_second_connected_evs = []; % TODO: initialize it already with the size of sorted_stored_values
    old_no_connected_EVs = 0;    
    
    for this_row = sorted_stored_values.'
        new_ts = this_row(1);
        slotid = this_row(3);
        no_connected_EVs = this_row(4);
        departure_time = this_row(5);
        energy_demand = this_row(6);
       
        while current_ts < new_ts
            per_second_connected_evs = [per_second_connected_evs; current_ts old_no_connected_EVs];         
            current_ts = current_ts + 1;
        end
        old_no_connected_EVs = no_connected_EVs;
    end
    
    while current_ts <= 172800
        per_second_connected_evs = [per_second_connected_evs; current_ts old_no_connected_EVs]; 
        current_ts = current_ts + 1;
    end
    
    per_second_connected_evs_single_day = per_second_connected_evs(86401:end,2:2);
        
end