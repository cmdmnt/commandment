Installation
============

macOS
-----

Requirements:

    - **Python 3.5+**
        - If you have Homebrew, you can install this by running ``brew install python3`` at a terminal prompt.
          This will not overwrite any Python 2.X installations.
    - **Commandment Source**
    - **MDM Push Certificate** either as a single ``.pem`` file or as a **PKCS#12** ``.p12`` file, which will be
      converted at launch.
    - A running **SCEP Service**. `SCEPy <https://github.com/mosen/SCEPy>`_ is available as a test implementation,
      also as a `docker container <https://hub.docker.com/r/mosen/scepy/>`_.

