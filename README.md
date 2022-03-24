# LP_MERCARI_MS_calendar_T10


The Calendar Microservice contains the methods to check and fill slots for the doctors as well as labs. This Microservice uses MongoDB as the database, owing to the relational structure of the data. This dabase has a separate document(MongoDB) for each doctor, as well as contains methods to add a new doctor database, in order to make the system scalable.

The various endpoints contained in this microservice are :

- `/fill_lot` :  This endpoint is used to book slots for the patients. 

- `/removeSlot` : This endpoint is used to delete a particular slot by the doctor.

- `/checkAvailable` : This endpoint is used to check the availability of time slots for a particular doctor, given a start time and duration of the appointment
