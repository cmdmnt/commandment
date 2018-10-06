DEP (Device Enrollment Program)
===============================

This document outlines configuration of the DEP device syncing service.
This information applies to classic DEP as well as Apple School Manager and Apple Business Manager.

Configuring via the UI
----------------------

- Click on **Settings** -> **DEP Accounts**.
- **New DEP Account**
- Click on the **Download** button to begin downloading a Public Key.
    You will use this to upload to Apple Business Manager [#abm]_ or Apple School Manager [#asm]_.
- Create a new **MDM Server** in ASM or ABM, as described in the ASM Help `here <https://help.apple.com/schoolmanager/#/asm1c1be359d>`_.
- Upload the :file:`commandment-dep.cer` file you just downloaded, using the **Upload Key** button.
- Download the DEP token using the **Get Token** link.
- Unfortunately, for now you will have to upload the token using the **curl** command as outlined in API step 5.

Configuring via API
-------------------

1. Make a *GET* request to ``/dep/certificate/download`` to download the initial DEP Public Key. The public key is
	generated on request, and stored in the database with name ``COMMANDMENT-DEP``.
2. Perform the manual process of Adding an ASM/ABM **MDM Server**, and uploading the certificate you retrieved in step 1.
3. Download the DEP token from ASM/ABM, which will be a file ending in ``_smime.p7m``.
4. Upload the file to ``/dep/stoken/upload`` as multipart/form-encoded with the file field of **file**, the equivalent
	curl command line would be::

	curl -F 'file=@/path/to/_smime.p7m' https://commandment.local/dep/stoken/upload

5. The DEP token should be decrypted, and devices should start appearing when the next DEP sync happens or when the
	server is restarted.


.. rubric:: Footnotes

.. [#abm] Apple Business Manager
.. [#asm] Apple School Manager, available at https://school.apple.com

