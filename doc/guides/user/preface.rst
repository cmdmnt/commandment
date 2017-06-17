Preface
=======

Setting up an MDM requires a few different certificates:

- To prove to Apple who you are (Push).
- To prove that your MDM isn't being impersonated (TLS).
- To prove that someone isn't impersonating an Apple Device connecting to your MDM (SCEP/Identity Certificate).

.. note:: I'm glossing over a lot of detail to give you an overview.

By far, the best explanation is the MicroMDM Blog post by Jesse Peterson on
`Understanding MDM Certificates <https://micromdm.io/blog/certificates/>`_.

APNS MDM Certificate
--------------------

Apple devices listen for Push Notifications, sent via Apple's Push Notification Service [#f1]_.
The notifications you send from your MDM are used to poke the devices, which contact your MDM in turn.

To send MDM push notifications, you will need a special Push Certificate issued by Apple.

There are several ways to get one:

- Apply for an `Apple Enterprise Developer <https://developer.apple.com/programs/enterprise/>`_ account (US$300/year),
  enabling the MDM Vendor option. You can then use this account to sign push certificate requests.
- Have an MDM vendor, or someone with that account sign the CSR for you. `mdmcert.download <https://mdmcert.download>`_
  is one such service.
- Server.app



.. rubric:: Footnotes

.. [#f1] `Push Notification Guide <https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/APNSOverview.html#//apple_ref/doc/uid/TP40008194-CH8-SW1>`_.