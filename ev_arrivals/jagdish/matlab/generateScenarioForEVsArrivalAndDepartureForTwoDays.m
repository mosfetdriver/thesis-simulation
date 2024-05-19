function sorted_stored_values = generateScenarioForEVsArrivalAndDepartureForTwoDays(time_slots_for_arrival_rate_in_hrs, arrival_rates_hourly_for_cs_with_100_slots, no_charging_slots, mean_energy_demand, interval_energy_demand, mean_stay_time, interval_stay_time)
    current_time = 0;
    time_slots_for_arrival_rate_in_secs = time_slots_for_arrival_rate_in_hrs * 3600;
   
    arrival_rates_hourly = arrival_rates_hourly_for_cs_with_100_slots * no_charging_slots / 100;
    arrival_rates_secondly = arrival_rates_hourly / 3600;
    max_rate = max(arrival_rates_secondly);
    occupied_slots = containers.Map;
    keySet = {'time_to_leave', 'energy_demand'};
    stored_values = []; % timestamp arrival(1)/departure(0) slotid noConnectedEVs departureTime energyDemand
    while 1
        arrival_time = -log(1.0 - rand) / max_rate;
        current_time = current_time + arrival_time;
        
        % departure logic
        for slot = keys(occupied_slots)
            internal_dict = occupied_slots(slot{1});
            
            if internal_dict('time_to_leave') <= current_time && internal_dict('time_to_leave') <= 172800 
                time_to_leave = internal_dict('time_to_leave');
                %fprintf('time_to_leave is %f, slot is %s, number of occupied slots are %d.\n', time_to_leave, slot{1}, occupied_slots.Count - 1);
                stored_values = [stored_values; time_to_leave 0 str2double(slot{1}) occupied_slots.Count - 1 0 0];
                remove(occupied_slots, slot);
            end
        end 
        
        % simulate only two days
        if current_time > 172800
            break
        end
        
        if rand <= rate(current_time) / max_rate && occupied_slots.Count < no_charging_slots
            slot_to_use = '';

            for slot = 1: no_charging_slots
                if ~isKey(occupied_slots, int2str(slot))
                    slot_to_use = int2str(slot);
                    break
                end
            end

            time_to_leave = current_time + ((mean_stay_time + interval_stay_time - (mean_stay_time - interval_stay_time)).*rand + (mean_stay_time - interval_stay_time)) * 3600; % in seconds
            energy_demand = (mean_energy_demand + interval_energy_demand - (mean_energy_demand - interval_energy_demand)).*rand + (mean_energy_demand - interval_energy_demand); % in kWh
            valueSet = [time_to_leave energy_demand];
            occupied_slots(slot_to_use) = containers.Map(keySet, valueSet);
            %fprintf('slot_to_use is %s, current_time is %f, the number of occupied slots are %d, time_to_leave is %f, energy_demand is %f.\n', slot_to_use, current_time, occupied_slots.Count, time_to_leave, energy_demand);
            stored_values = [stored_values; current_time 1 str2double(slot_to_use) occupied_slots.Count time_to_leave energy_demand];
        end
    end  
    
    sorted_stored_values = sortrows(stored_values, 1);
    
    
    function rate_value = rate(time) % time is in seconds
        time = rem(time, 86400);
        i = 1;
        size_time_slots = size(time_slots_for_arrival_rate_in_secs, 2);

        while time > time_slots_for_arrival_rate_in_secs(1, i)
            i = i + 1;
            if i > size_time_slots
                break
            end
        end
        i = i - 1;

        rate_value = arrival_rates_secondly(i);
    end

end