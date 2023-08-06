from django.core.exceptions import ValidationError

from web3 import Web3


def validate_checksumed_address(address):
    address = Web3.toAddressChecksum(address.lower())
    if not Web3.isChecksumAddress(address):
        raise ValidationError(
            '%(address)s has an invalid checksum',
            params={'address': address},
        )
