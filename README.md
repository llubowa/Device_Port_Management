# Port-status-app
Application is for managing ports on network devices
The network devices are core hubs and aggregation hubs.
Each aggregation hub can have extensions of at maximum 3 more switches. The extension switches are called Cascaded
The application manages the description of the ports on each device in the following ways;
1) You can check the status of the ports i.e used or free
2) You can change the description on the port or change the status of the port from used to free or vice versa.
This application is built with python using Django framework. MySql is the database used for this project.
Currently the fully buit up app/section is the one which deals with aggregation hubs
