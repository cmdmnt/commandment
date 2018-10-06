About MDM
=========

This section is intended to give you some basic knowledge around how MDM works, so that you understand why some of
the prerequisites exist.

Setting up an MDM requires a few different certificates:

- To prove to Apple that you're allowed to use their Push Service (APNS).
- To prove that your MDM isn't being impersonated (TLS).
- To prove that someone isn't impersonating an Apple Device connecting to your MDM (SCEP/Identity Certificate).

.. note:: I'm glossing over a lot of detail to give you a general sense of the requirements.

By far, the best in-depth explanation is the MicroMDM Blog post by Jesse Peterson on
`Understanding MDM Certificates <https://micromdm.io/blog/certificates/>`_.

APNS MDM Certificate
--------------------

Apple devices listen for Push Notifications, sent via Apple's Push Notification Service [#f1]_.
The notifications you send from your MDM are used to poke the devices, which contact your MDM in turn.

.. uml::
    :align: center

    "Joe's iPad" <-> "Apple Push Notification Service": Listening to MDM channel
    MDM -> "Apple Push Notification Service": Push to "Joe's iPad"
    "Apple Push Notification Service" -> "Joe's iPad": Hey, contact the MDM!
    "Joe's iPad" -> MDM: Give me the next command!

To send MDM push notifications, you will need a special Push Certificate issued by Apple.

There are several ways to get one:

- Apply for an `Apple Enterprise Developer <https://developer.apple.com/programs/enterprise/>`_ account (US$300/year),
  enabling the MDM Vendor option. You can then use this account to sign push certificate requests. The MDM Vendor option
  is now available as a checkbox when you apply for the account.
- Have an MDM vendor, or someone with that account sign the CSR for you. `mdmcert.download <https://mdmcert.download>`_
  is one such service.
- Extract the *com.apple.mgmt.* certificate from a previously installed copy of **Server.app**

TLS/Web Certificate
-------------------

The MDM protocol requires a secure encrypted connection between your devices and your MDM.

The TLS certificate on your MDM is just like any other web server, so all the same methods apply for getting one of
these certificates.

It's recommended to purchase an SSL certificate that will already be trusted by your devices. You can also use an
Enterprise CA, as long as you understand that there's an extra step to allow your devices to trust the CA.

.. warning:: If you are using a self-signed SSL certificate, or your Enterprise CA won't automatically be trusted by
    your devices, then you need to make sure your devices trust the certificate. This is normally done by pushing a
    trust profile or including trust information in the enrollment profile.

    commandment has an option to bundle these certificates with the enrollment profile.


Device Identity Certificate
---------------------------

The MDM protocol requires that each device enrolled with the MDM has its own certificate.

There are two options for providing the identity certificate:

- Include the Identity certificate in the enrollment payloads.
- Contact a SCEP service to issue a certificate when the device enrolls.

The second option is always the preferred method, since it allows you to use whatever existing infrastructure you have
for issuing certificates.

If you are testing commandment you can use `SCEPy <https://github.com/cmdmnt/SCEPy>`_ as your SCEP server.
This is provided as part of commandment for testing out of the box, but I would strongly encourage you to use a
commercial solution for SCEP.


.. rubric:: Footnotes

.. [#f1] `Push Notification Developer Guide <https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/APNSOverview.html#//apple_ref/doc/uid/TP40008194-CH8-SW1>`_.