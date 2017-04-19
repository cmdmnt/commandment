## Requirements

##### Software Requirements

* [Python](https://www.python.org/) 2.7+
* [cryptography](https://cryptography.io/en/latest/)
* [Flask](http://flask.pocoo.org/)
* [SQLAlchemy](http://www.sqlalchemy.org/)
* [SQLite](https://www.sqlite.org/) (default database)

##### Apple MDM push notification certificate

You will need an Apple MDM APNs certificate in order to send MDM push notifications to devices. To get one, for now, you'll need to have an [Apple Enterprise Developer](https://developer.apple.com/programs/enterprise/) account (US$300/year).

Eventually this software may support an ability to assist in getting one of these Push Certificates from Apple's servers. But for now please read [Pepijn Bruienne's excellent blog post](http://enterprisemac.bruienne.com/2015/06/06/mdm-azing-setting-up-your-own-mdm-server/) on how to get this certificate. Note that that post includes information on setting up [Project iMAS MDM server](https://github.com/project-imas/mdm-server) and so some of his post isn't directly relevant to getting the Apple push certificate.

Note we don't yet deal with any intermediate steps or certificates with this MDM software (such as Vendor MDM Certificates or generating and submitting CSRs to Apple, etc.). Those steps are required, but they have little to do with running this software. We just require the very end product of the actual MDM push certificate (certificate subject that contains `com.apple.mgmt.*` and associated private key). It needs to be an unencrypted certificate and private key in PEM form for later import into the MDM server. This may require an additional export and unencryption of the exported certificate.

##### DNS and network configuration for SSL hostname matching

It is possible to use self-signed certificates with an Apple MDM system. However the hostname and SSL certificate subject matching is strict and an enrolling device needs to trust the MDM server's HTTPS certificate.

The trust is established when the device enrolls: by default the HTTPS certificate is included as a profile payload for the device to trust when enrolling. However the hostname matching still needs to be successful. Practically speaking this means that if you intend for your devices to access your MDM via something like https://mymdm.example.com:5443/ then the MDM's web server certificate must also "match" this name (in typical SSL matching rules which includes wildcards and such) by having a certificate subject Common Name (CN) of `mymdm.example.com`.

If you have a DNS record already setup and don't want to use the default `mymdm.example.com` name then you'll need to generate a new web server certificate. Instructions for doing so are below, **but remember to restart the development webserver** after you've *generated a new* web certificate with an appropriate Common Name (CN) and *deleted the old* web certificate.

While not recommended it's possible to use a `/etc/hosts` entry to test the system including enrollment and MDM operation of a single system on the same host as the server. Useful for quick and dirty virtual machine testing.

_**Note:** while IP address certificates appear to work for MDM on iOS not much luck was had with OS X doing this. Besides this it is [not recommended](http://tools.ietf.org/html/rfc6125#section-1.7.2) to use IP addresses in the Common Name field for certificates. Also the CA/B has [deprecated](https://cabforum.org/internal-names/) *internal* IP addresses in certificate subjects from public Certificate Authorities. In other words: best not to go this route._

## Installing the requirements

#### Setting up on OS X for development and testing in a Python virtual environment

Instructions for OS X 10.10. These aren't definitive instructions for getting the dependencies installed on OS X. See also [Greg Neagle's post](https://groups.google.com/d/msg/ossmdm/onF7KFWnIa4/LMMRu7OrBiIJ) on getting Project IMAS requirements setup (which are similar to our requirements).


##### Install & create virtualenv

[virtualenv](https://virtualenv.pypa.io/en/latest/) is a tool to create isolated Python environments. We want to use this so we're not installing Python packages to the system Python locations and to have a self-contained Python environment. We do have to install virtualenv to the system locations, however:

```bash
sudo easy_install virtualenv
```

Then, create the virtualenv and import the configuration into the current shell:

```bash
virtualenv commandment-venv
source commandment-venv/bin/activate
```

After `source`ing the virtualenv your bash prompt should have changed to include the `commandment-venv`. From:


```bash
Mac:Desktop jesse$
```

To:

```bash
(commandment-venv)Mac:Desktop jesse$
```

##### Clone the source

Use Git to clone the GitHub source of commandment:

```bash
git clone git@github.com:jessepeterson/commandment.git
cd commandment
```

##### Install Python project dependencies 

While still in the `commandment-venv`-activated virtualenv, and in the `commandment` checked-out source code directory, tell `pip` to install the requirements:

```bash
pip install -r requirements.txt
```

Assuming all of the above steps completed without problems you should be good to go now. Next steps are to run the server and begin in-webapp configuration.

For OS X 10.9 users: M2Crypto can't find the OpenSSL header files on the system. To get around this download the latest tarball of [M2Crypto from PyPi](https://pypi.python.org/pypi/M2Crypto), unpack it, change to it's directory, and while still in the virtualenv run:

```bash
python setup.py install build_ext --openssl=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk/usr
```

Then re-run the `pip -r` command from above to get the rest of the dependencies which should install fine.

## Server installation and setup

### 1. Start runserver.py and visit web site

```bash
./runserver.py
```

This will immediately configure application settings, setup the database's ORM (SQLAlchemy), create the database schema (in the default SQLite database `mdm.db` in the current directory), create initial self-signed SSL certificates and keys, configure the development web server and start the application. Soon after start it should start listening on the default port 5443 and amongst the verbose output should be these lines:

```
 * Running on https://0.0.0.0:5443/ (Press CTRL+C to quit)
 * Restarting with stat
```

This means the server has started and is listening for connections. Go visit https://127.0.0.1:5443/ (remembering the http**S**:// as it is a secure site). You'll get an SSL certificate warning prompt as the server is using a newly generated self-signed certificate. But you can ignore that for now and continue to the site.

You should be presented with the enrollment interface. Don't try to enroll devices yet or click on the enroll link. We're not setup yet.

### 2. Add your push certificate to the system

Per the above requirements you'll need your Apple MDM push certificate and private key in unencrypted PEM form. Once you have those then visit https://127.0.0.1:5443/admin/certificates. You should be presented with a list of all the non-device identity certificates currently configured in the system. One of items listed will be "APNS MDM Push Certificate (Required)" and a "(Certificate Missing)" in red where the subject would be. To the right of this table row click the "[ Add ]" link. This will give us two large text fields to paste in the PEM certificate and private key into the system. Do so and click Submit. If all worked then you should now see that the Subject column of the APNS MDM Push Certificate row is filled in with a `UID=com.apple.mgmt.*, CN=APSP:*` entry where the asterisks are UUID-looking values. The APNS certificate is now in the system ready for use.

### 3. Setup an appropriate web server SSL certificate and verify

Per the above requirements you're likely not going to use the default server name of `mymdm.example.com`. So we'll want to generate ourselves a more appropriate self-signed certificate. This can be done in the app itself. Visit the admin certificates page again. You should see the default `CN=mymdm.example.com` certificate under the "MDM Web Server Certificate". Before you delete this certificate realize that without a proper web certificate the development server cannot start. Delete the `CN=mymdm.example.com` certificate and then click the "[ Generate New ]" link to make a new one. The only type of certificate (currently) allowed that you can create is a web server certificate. Fill in the various fields of the of the new certificate but **importantly** using a Common Name that matches the DNS name of the server.

Now **restart the web server** (press controll-C in the server Terminal) to start using this new certificate. Navigate to your server URL using the new DNS name that you just created and the same port number. As an example if we used `newtestmdm.example.com` to generate a certificate then navigate to https://newtestmdm.example.com:5443/. You should still get a browser prompt for a certificate (it is still a self-signed certificate) but the name of the certificate should be the new name that you gave it when you generated the certificate. Verify this when the certificate prompt comes up. For our example here the certificate subject common name would be `newtestmdm.example.com`. If it does not match the URL you're using then expect problems enrolling devices and using the MDM server.

### 4. Create MDM certificate configuration

Now that we have correct DNS & web server certificate, we need to create the MDM configuration. In the web admin click the "Config" link at the top. Fill out the form as it's page describes. The Profile prefix is often just the domain name in reverse "domain component" form. For our example this might be "com.example.newtestmdm". Take special care for the hostname and web server port. This field should match the hostname used for the web server certificate above, and the same port number (default 5443). There should only be one Certificate Authority and Push Certificate available to select at this stage. ***Keep in mind** that the MDM Push certificate "topic" and hostname/port (MDM URLs) cannot change for the lifetime that a device is enrolled: this is a specific requirement of MDM profile payloads.* Now Click Submit. The Config Admin page should reload but now with some values statically set.

You should now be able to enroll a device!

### 5. Enroll a device

_**WARNING:** It goes without saying MDM systems are powerful. They can lock, wipe, or otherwise disable a device. It's recommended to test using a device that is not important in case of accidental or inadvertant data loss or lock-out (which would require a reset)._

On a device to be enrolled go to the landing page of the MDM system. This is the root URL we accessed above. In our example this is https://newtestmdm.example.com:5443/. Click the link to enroll. This will dynamically generate an MDM enrollment profile that should trust the web server certificate, includes the device's newly generated identity certificate (signed by the built-in CA), the MDM payload, and enroll the device.

If the device was successfully enrolled then you should be able to visit the devices list (https://newtestmdm.example.com:5443/admin/devices in our example setup) to view the newly enrolled device. Sometimes the very first MDM notification is not sent (and thus the device details are missing from the table) so the "[ Send Push Notif. ]" button can be used to request the machine specifically check-in.

Congrats! If it enrolled and you see device details (name, serial number, etc.) then it's working! Now something a little more useful..

_**Warning:** Apple recommends MDM developers use a SCEP system to enroll certificates with an MDM vendor. To simplify setup we do not do this and instead generate a device identity certificate directly embedded in the enrollment profile. For iOS this is likely fine as the enrollment profile isn't by default downloaded anywhere. But on OS X the enrollment profile is downloaded to disk (default browser action) which means the device's identity certificate is stored on the filesystem trivially accessible (usually just in the Downloads folder). Given access to the enrollment profile one can trivially spoof the device to the MDM system. This means you may want to enroll OS X devices using a script or other technique than just having users simply enroll to make sure the original enrollment profile is deleted after enrollment. The device identity private key is not stored in the MDM server after the enrollment profile is generated but it is embedded in the enrollment profile._

### 6. Create a device group and apply a (the) example profile to it

From the admin area of the web app go to the Groups page. Add a group naming it however you wish. Now go to the Profiles admin page. Create a new one. Uncheck the "Allow iTunes" checkbox (note this profile only does anything on iOS devices). And click Add Profile. Edit this newly created Profile. Select the newly created group under the Group Applicablility section. You've now associated that profile to be installed on any devices in that group.

### 7. Assign the device to this group to apply the profile to it

Go to the Devices list. Click the "[ View Device ]" link for your newly enrolled device. Select the newly assigned profile group you created and click the 'Update Device Group' link. Performing this action will create the new group membership, queue a new MDM command to install the profile on the device, and send a push notification to the device to run this command.

If all worked then the iOS device you enrolled should have it's iTunes icon removed from it's home screen. You should be able to unassign the device from the group to put it back.

*Currently only device group memebership triggers profile updates, further functionality is coming.*
