
% Variable to use
TIME_SLOTS_FOR_ARRIVAL_RATE_IN_HRS = [0 8 12 18 20; 8 12 18 20 24];
ARRIVAL_RATES_HOURLY_FOR_CS_WITH_100_SLOTS = [20 90 30 150 25]; %[20 90 30 150 25] used in Python
PMAX_EV = 30; % kW
MEAN_ENERGY_DEMAND = 100; % kWh
INTERVAL_ENERGY_DEMAND = 20; % kWh
MEAN_STAY_TIME = 5; % hours
INTERVAL_STAY_TIME = 0.5; % hours
NO_CHARGING_SLOTS = 5;  % number of EVs that can be charged simultaeneously

disp('Generating Scenarios...');
sorted_stored_values = generateScenarioForEVsArrivalAndDepartureForTwoDays(TIME_SLOTS_FOR_ARRIVAL_RATE_IN_HRS, ARRIVAL_RATES_HOURLY_FOR_CS_WITH_100_SLOTS, NO_CHARGING_SLOTS, MEAN_ENERGY_DEMAND, INTERVAL_ENERGY_DEMAND, MEAN_STAY_TIME, INTERVAL_STAY_TIME);
disp('Scenario Done!');

disp('Computing SecondDayProfileOfNoEVsPerSecond...');
per_second_connected_evs_single_day = computeSecondDayProfileOfNoEVsPerSecond(sorted_stored_values);
disp('SecondDayProfileOfNoEVsPerSecond Done!');

disp('Computing SecondDayPredictionProfileOfNoEVsPerSecond...');
[per_15min_min_connected_evs_single_day, per_15min_max_connected_evs_single_day, per_15min_mean_connected_evs_single_day] = computeSecondDayPredictionProfileOfNoEVsPer15Minutes(per_second_connected_evs_single_day);
disp('SecondDayPredictionProfileOfNoEVsPerSecond Done!');

disp('Computing MatricesForInputToSolver...')
[per_second_mask_single_day, per_second_deltaT_single_day, per_second_deltaE_single_day] = computeMatricesForInputToSolver(sorted_stored_values, NO_CHARGING_SLOTS, PMAX_EV);
disp('MatricesForInputToSolver Done!')

disp('Job done!');
save('10April2018');
