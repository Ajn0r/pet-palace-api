# Pet Palace API

## Apps

The Pet Palace API has got # nr of apps, the different apps and their purpose is described as follows:

### Profile app

An app for the user's profile, the profile is created automatically when they sign up and create a user, they cannot delete the profile, only update it.

The profile model holds information about the user,
such as name, description of them, profile image, if they are a pet owner or not,
and when the profile was created and updated.

## Setting up the project

I have followed the Code Institutes template from the Django rest DRF_API walkthrough to set up the project with Django and Cloudinary.

1. The first step was to use the Code institute full template to create a new repository and open it in Gitpod.

2. Installing Django from the terminal `pip3 install 'django<4'`

3. Create a project: `django-admin startproject pet_palace_api`

4. Cloudinary libraries to manage static files `pip install django-cloudinary-storage`

5. Add Pillow for image processing `pip install Pillow`

6. Add cloudinary to INSTALLED_APPS

7. Create an env.py file and import os `import os`

8. Set the url variable value `os.environ['CLOUDINARY_URL'] = 'cloudinary://my-API-Environment-variable'`

9. Import os and add if statement in setting.py
```
import os
if os.path.exists('env.py'):
    import env

```

10. Setting the CLOUDINARY_STORAGE variable to equal the CLOUDINARY_URL variable 
```
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ.get('CLOUDINARY_URL')
}
```

11. Add media storage URL `MEDIA_URL = '/media/'`

12. Set default file storage to cloudinary 
```
DEFAULT_FILE_STORAGE = 
    'cloudinary_storage.storage.MediaCloudinaryStorage'
```

Now the basic project was finished, the next step were to start setting up all the apps and adding them to the settings.py file.

## Testing

### Profile app

In the profile app, there was one automated test to make sure that a profile was created for every new user.

![testcaseprofiles](/documentation/testing/profilecreatetest.png)

The test failed the first time due to that there were three users created and the test only expected two profiles,
when changed to expect three profiles instead the test was successful.

![testcaseprofileresult](/documentation/testing/testprofileresult.png)