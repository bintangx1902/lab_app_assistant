# What tools has been provided

1. Delete cache (run this in terminal)
> python manage clearcache
> 
> pyclean .

2. Delete Other user (in terminal)
> python manage.py shell 

```python
from django.contrib.auth.models import User
users = User.objects.filter(is_staff=False) 
for u in users: 
    u.delete()
```

3. Delete all the presence QR
> python manage.py shell 

```bash
cd <lab_folder_name>
sudo rm -r media/qr/*
```

4. Re-Saving the QR after update
> python manage.py shell 

```python
from presence.models import *
qr = GenerateQRCode.objects.all() 
for x in qr:
    x.save()
```
this code is gonna resave after the load data process

5. How to backup <br>
   1. go to terminal
   2. activate the virtual environment you create
   3. go to lab folder `cd <lab_folder_name>`
   4. ```bash 
      python manage.py dumpdata > load.json
      ```
   5. look for the file named load.json
   6. copy to home 
      ```bash
      sudo cp load.json ~  
      ```

6. How to Update and load data <br>
   1. go to terminal
   2. activate the virtual environment you create
   3. delete old lab folder by using `sudo rm -r <lab_folder_name>`
   4. clone the new from github `git clone https://your-git.link`
   5. go to lab folder `cd <lab_folder_name>`
   6. Copy the json file in home ``sudo cp ~/load.json .``
   7. ```bash 
      python manage.py loaddata load.json
      ```
