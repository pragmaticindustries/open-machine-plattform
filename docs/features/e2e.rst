End to End (E2E) Encrypted Messages
-----------------------------

End to End Encrypted messages or telemetry values are a rather new feature of the OMAP.
The idea is, that some telemetry values can be encrypted by the edge device before being send to the platform.
Then, the values can be consumed by another application or user on the platform and are then decrypted.
So the operator and owner of the platform can technically never read the values.

Why can such a feature be useful?
Its an approach towards zero-trust. Producers may be uncomfortable by sharing sensible data like concrete production numbers with any third party. But in scenarios like e.g. progressive payment models like pay-per-use they may have the need to share the data with a bank or any other financial provider.
In this scenario E2E telemetry comes in handy.
As the Machine Owner can be sure that only he and the receiving party, the financial provider can access and understand the data and the operator of the platform cannot read or modify the data in any way.

In the OMAP E2E is implemented based on the `OLM <https://gitlab.matrix.org/matrix-org/olm/-/blob/master/README.md>`_ / `MEGOLM <https://matrix.org/docs/spec/client_server/r0.4.0.html#m-megolm-v1-aes-sha2>`_ protocol used in popular open source messaging solutions like `Signal <https://signalfoundation.org/>`_ and `Matrix <https://matrix.org/>`_.
The OLM Algorithm is based on the `Signal Protocol <https://signal.org/docs/specifications/doubleratchet/>`_ developed initially by Trevor Perin and Moxie Marlinspike at OpenWhisperSystems.

A major difference between a messaging protocol and the telemetry use case is that handshakes are not possible or at least very rarely possible.
Thus, we base the E2E on the MEGOLM algorithm which was developed for securing group chats over the matrix protocol and needs no handshakes but only the secure transmission of a secret key.

