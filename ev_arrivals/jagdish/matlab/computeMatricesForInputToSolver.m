function [per_second_mask_single_day, per_second_deltaT_single_day, per_second_deltaE_single_day] = computeMatricesForInputToSolver(sorted_stored_values, no_charging_slots, pmax_ev)
    current_ts = 1;
    
    per_second_mask = []; % TODO set the size already?
    row_no_charging_slots = zeros(1, no_charging_slots, 'uint8');
    
    per_second_deltaT = []; % TODO set the size already?
    row_deltaT = zeros(1, no_charging_slots, 'uint32');
   
    per_second_deltaE = []; % TODO set the size already?
    row_deltaE = zeros(1, no_charging_slots);
    
    for this_row = sorted_stored_values.'
        new_ts = this_row(1);
        isArrival = this_row(2);
        slotid = this_row(3);
        departure_time = this_row(5);
        energy_demand = this_row(6);
       
        while current_ts < new_ts
            
            % mask will only change with arrival/departure
            per_second_mask = [per_second_mask; row_no_charging_slots];
            
            % deltaT will just decrease by 1 for all slots except with
            % value 0
            row_deltaT = max(row_deltaT - 1, 0);
            per_second_deltaT = [per_second_deltaT; row_deltaT];
            
            % deltaE will just decrease by pmax_ev / 3600
            row_deltaE = max(row_deltaE - pmax_ev / 3600, 0);
            per_second_deltaE = [per_second_deltaE; row_deltaE];
            
            current_ts = current_ts + 1;
        end
        
  
        if isArrival
            % flip 0 to 1 at this slot
            row_no_charging_slots(1, slotid) = 1;
            
            % compute the stay time
            row_deltaT(1, slotid) = (departure_time - new_ts) + 1;
            
            % put the initial energy demand
            row_deltaE(1, slotid) = energy_demand;
        else
            % flip 1 to 0 at this slot
            row_no_charging_slots(1, slotid) = 0;
            
            % put it to zero
            row_deltaT(1, slotid) = 0;
            
            % put it to zero
            row_deltaE(1, slotid) = 0;
        end
    end
    
    while current_ts <= 172800
          
        % mask will only change with arrival/departure
        per_second_mask = [per_second_mask; row_no_charging_slots];
        
        % deltaT will just decrease by 1 for all slots except with
        % value 0
        row_deltaT = max(row_deltaT - 1, 0);
        per_second_deltaT = [per_second_deltaT; row_deltaT];

        % deltaE will just decrease by pmax_ev / 3600
        row_deltaE = max(row_deltaE - pmax_ev / 3600, 0);
        per_second_deltaE = [per_second_deltaE; row_deltaE];
        
        current_ts = current_ts + 1;
    end
    
    per_second_mask_single_day = per_second_mask(86401:end,:);
    
    per_second_deltaT_single_day = per_second_deltaT(86401:end,:);
        
    per_second_deltaE_single_day = per_second_deltaE(86401:end,:);
  
end