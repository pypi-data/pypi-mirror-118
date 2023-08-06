from clearlife.cli import get_default_args, main


__version__ = '0.2.0'  # also change in setup.py


class ClearLifeClient(object):
    """API Client for interacting with the `clearlifed` API
    endpoints. Note that this object is just a wrapper around
    the commands in :mod:`clearlifed.cli`.
    """
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.args = get_default_args(name)

        self._otp = None
        self._app_keys = None


    @property
    def otp(self):
        """Registers this server application with `clearlifed` to
        obtain end-to-end encryption keys.
        """
        if self._otp is None:
            args = self.args.copy()
            args.update({
                "command": "register",
            })

            self._otp = main(args)

        return self._otp


    @property
    def app_keys(self):
        if self._app_keys is None:
            args = self.args.copy()
            args.update({
                "command": "appkeys",
                "seed": self.otp["seed"]
            })
            self._app_keys = main(args)

        return self._app_keys


    def derive(self, context, keyid):
        """Derives the keypair and seed for the given context
        and keyid.
        """
        args = self.args.copy()
        args.update({
            "command": "derive",
            "context": context,
            "keyid": keyid,
            "seed": self.otp["seed"]
        })

        return main(args)
