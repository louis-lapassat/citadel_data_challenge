# The Data Open London - Citadel - 2020

This is the code and report of team 12 composed of: Khaoula Belahsen, Louis Lapassat, Louis Serrano and Jean-Noël Tuccella. We won third place. The main challenge of this competition was to find your own question/problematic and verify/explain your ideas using the provided datasets.

**Topic question: What suggestions can we provide in order to optimize the management of bike allocation based on an in-and-out flow analysis across the bike share network?**

**Abstract**: we focus here on bike flows between two stations (start station and end station) in New York City. The main idea is to emphasize that some stations are highly stressed (because of huge difference of incoming and outgoing flows) and thus potentially it creates bottleneck in the network. In practice, this may lead to a surplus of bikes at a given station or the opposite (a customer may not find a bike). Therefore we first propose to analyze the stations (stress cluster, positions, etc.) and finally we create a toy model to predict flow imbalance (using ARIMA) for each cluster in order to takle the problem (could be used to map agents to redistribute the bikes, redirect customers to another station, etc.).
