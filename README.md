# Meeting room occupancy predictor

A model for predicting if a meeting room will be occupied

## Why?

30% of the average energy used in commercial buildings is wasted [1], and studies have indicted occupancy has a large impact on energy consumption [2]. Understanding occupancy trends can improve a buildings energy consumption, therefore reducing costs and benefitting the environment. 

The majority of research into occupancy detection and prediction focuses on office rooms. The structure of meeting room occupancy deviates from average office rooms due to a seemingly unpredictable nature of peoples decisions to use them. Research shows that 33% of meetings are unplanned, 20% of booked meeting rooms are not used, and people waste 2.2% of their day searching for a free room [3]. This has highlighted the opportunity to better understand these statistics and how they affect meeting room occupancy - thus benefitting employees, managers and energy savings of buildings.

An abundance of research exists to investigate the plausibility of accurately predicting room occupancy based on a number of factors, such as Wi-Fi and environmental sensors (CO2, temperature etc). However it costs $147,000 to supply a five story building with sensors [4]. This large sum could be unattractive to managers of buildings and a more cost effective alternative needs to be sought. Utilising an existing infrastructure such as Wi-Fi is a valid suggestion to solve this problem. Research shows it is possible to accurately predict occupancy by utilising a Wi-Fi framework [5] [6], however this would require every occupant of a building to possess a Wi-Fi enabled device. Therefore, to my knowledge, there is not a solution currently to detect and predict occupancy that utilises an existing framework, and, does not require all occupants to possess a certain type of device. My project explores the possibility of creating this solution, by constructing an algorithm which can ascertain the likelihood a meeting room is occupied based on a number of factors.

## Results

The decision tree model correctly identified unoccupied rooms 99% of the time and occupied rooms 87% of the time. These high percentages display that there is a trend in the data, and it is possible to accurately predict future occupancy levels from this. Due to the historical training nature of the time series train-test split, the accuracy was produced from future data the model had never seen before. Below are two graphs to represent this:

These results are highlighted in the comparison between the ground truth occupancy and what the decision tree predicts the occupancy to be.

Ground truth: https://github.com/Alicetwhite/Meeting-room-occupancy-predictor/blob/master/Write_up/Actual-6hours.png

Predicted occupancy: https://github.com/Alicetwhite/Meeting-room-occupancy-predictor/blob/master/Write_up/dt.png

## References

[1] - Newman, “How to improve energy efficiency in commercial buildings”
Retrieved from: https://www.telegraph.co.uk/business/energy-efficiency/improve-energy-efficiency-commercial-buildings/
Last accessed: 21/04/19

[2] -  Airaksinen (2011), “Energy use in day care centers and schools”
Retrieved from: https://www.scopus.com/record/display.uri?eid=2-s2.0-79959787233&origin=inward&txGid=4f310cd3f470a6088ff0485ae22f3e3b
Last accessed: 21/04/19

[3] - Smart Buildings magazine, “Illuminated, integrated and intelligent. Introducing the office of the future…now”
Retrieved from: http://www.smartbuildingsmagazine.com/features/illuminated-integrated-and-intelligent.-introducing-the-office-of-the-futur
Last accessed: 21/04/19

[4] - Erikson, Cerpa & Carreira-Perpiñán (2014), “Occupancy Modeling and Prediction for Building Energy Management"
Retrieved from: http://faculty.ucmerced.edu/mcarreira-perpinan/papers/tosn14.pdf
Last accessed: 21/04/19

[5] - Balaji, Xu, Nwokafor, Gupta & Agarwal (2013), “Sentinel: Occupancy Based HVAC Actuation using existing WiFi Infrastructure within Commercial Buildings” 
Retrieved from: http://mesl.ucsd.edu/site/pubs/Balaji_SenSys2013_Sentinel.pdf
Last accessed: 21/04/19

[6] - Wang, Chen & Song (2017), “Modeling and predicting occupancy profile in office space with a Wi-Fi probe-based Dynamic Markov Time-Window Inference approach”
Retrieved from: https://www.sciencedirect.com/science/article/pii/S0360132317303487
Last accessed: 21/04/19
