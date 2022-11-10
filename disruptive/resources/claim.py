from __future__ import annotations

from typing import Any, Optional, List, Tuple

import disruptive.outputs as dtoutputs
import disruptive.requests as dtrequests
import disruptive.errors as dterrors


class Claim(dtoutputs.OutputBase):
    """
    Namespacing for claim methods.

    Attributes
    ----------
    type : str
        Whether or not the claim is for a KIT or DEVICE.
    claimed_item : Claim.ClaimKit | Claim.ClaimDevice
        An object representing the kit or device claim.

    """

    KIT = 'KIT'
    DEVICE = 'DEVICE'
    CLAIM_ITEMS = [KIT, DEVICE]

    def __init__(self, claim: dict) -> None:
        """
        Constructs the Claim object by unpacking raw claim response.

        Parameters
        ----------
        claim : dict
            Unmodified claim response dictionary.

        """

        # Inherit from OutputBase parent.
        dtoutputs.OutputBase.__init__(self, claim)

        # Unpack attributes from dictionary.
        self.type: str = claim['type']
        self.claimed_item: Claim.ClaimKit | Claim.ClaimDevice = \
            self._resolve_type(claim)

    @classmethod
    def claim_info(cls, identifier: str, **kwargs: Any) -> Claim:
        """
        Get claim information for either a device
        or a kit by looking up an identifier.

        For sensors, the identifier can be found in either
        the QR code or printed directly on the sensor.
        For kits, the identifier can be found both as text
        and a QR code printed on the box.

        For more information, see the
        `REST API Claim Info Documentation <https://developer.disruptive-
        technologies.com/api#/Claiming%20Devices%20%26%20Kits/
        get_claim_info>`_.

        Parameters
        ----------
        identifier : str
            Unique identifier of the target Kit or Device.

        Returns
        -------
        claim : Claim
            Claim information about the requested Kit or Device.

        Raises
        ------
        TypeError
            If provided identifier is not str type.

        Examples
        --------
        >>> # Get claim information about a kit.
        >>> claim = dt.Claim.claim_info('<KIT_ID>')

        >>> # Get claim information about a device.
        >>> claim = dt.Claim.claim_info('<DEVICE_ID>')

        """

        if not isinstance(identifier, str):
            raise TypeError(f'Identifier must be str, got {type(identifier)}.')

        url = f'/claimInfo?identifier={identifier}'

        return cls(dtrequests.DTRequest.get(url, **kwargs))

    @staticmethod
    def claim(target_project_id: str,
              kit_ids: Optional[List[str]] = None,
              device_ids: Optional[List[str]] = None,
              dry_run: bool = True,
              **kwargs: Any,
              ) -> Tuple[List[Claim.ClaimDevice], List[Exception]]:
        """
        Claim multiple kits and/or devices to your project.

        Claiming a kit/device does two things. It starts the device
        subscriptions, where any pre-paid period will be activated.
        It also adds the devices to your project.

        For more information, see the
        `REST API Claim Documentation <https://developer.disruptive-
        technologies.com/api#/Claiming%20Devices%20%26%20Kits/
        post_projects__project__devices_claim>`_.

        Parameters
        ----------
        target_project_id : str
            Unique identifier of project into which you wish to claim.
        kit_ids : list[str], optional
            List of unique kit IDs to claim.
        device_ids : list[str], optional
            List of unique device IDs to claim.
        dry_run : bool, optional
            Default True.
            Test your claim request during development.
            No kits or devices will be claimed while True.
            Set to False in production or no devices will be claimed.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        devices : list[Claim.ClaimDevice]
            List of successfully claimed devices.
        errors : list[ClaimError]
            List of errors that occured during claiming.
            If list is empty, all devices were claimed successfully.

        Examples
        --------
        >>> # Do a dry_run where you simulate claiming a kit.
        >>> devices, errors = dt.Claim.claim(
        ...     target_project_id='<TARGET_PROJECT_ID>',
        ...     kit_ids=['<KIT_ID>'],
        ... )

        >>> # Do a dry_run where you simulate claiming three devices.
        >>> devices, errors = dt.Claim.claim(
        ...     target_project_id='<TARGET_PROJECT_ID>',
        ...     device_ids=[
        ...         '<DEVICE_ID_1>',
        ...         '<DEVICE_ID_2>',
        ...         '<DEVICE_ID_3>',
        ...     ],
        ... )

        >>> # Turn off dry_run and claim 2 kits and 3 devices.
        >>> # This action is not reversible.
        >>> devices, errors = dt.Claim.claim(
        ...     target_project_id='<TARGET_PROJECT_ID>',
        ...     kit_ids=[
        ...         '<KIT_ID_1>',
        ...         '<KIT_ID_2>',
        ...     ],
        ...     device_ids=[
        ...         '<DEVICE_ID_1>',
        ...         '<DEVICE_ID_2>',
        ...         '<DEVICE_ID_3>',
        ...     ]
        ...     dry_run=False,
        ... )

        """

        url = f'/projects/{target_project_id}/devices:claim'
        url += f'?dryRun={str(dry_run).lower()}'

        body = {}
        if kit_ids is not None:
            body['kitIds'] = kit_ids
        if device_ids is not None:
            body['deviceIds'] = device_ids

        res = dtrequests.DTRequest.post(url, body=body, **kwargs)

        return (
            [Claim.ClaimDevice(d) for d in res['claimedDevices']],
            Claim._parse_claim_errors(res['claimErrors']),
        )

    @staticmethod
    def _parse_claim_errors(res_errors: dict) -> List[Exception]:
        errors: List[Exception] = []
        for error in res_errors['devices'] + res_errors['kits']:
            if error['code'] == 'ALREADY_CLAIMED':
                errors.append(dterrors.ClaimErrorDeviceAlreadyClaimed(error))
            elif error['code'] == 'NOT_FOUND' and 'deviceId' in error:
                errors.append(dterrors.ClaimErrorDeviceNotFound(error))
            elif error['code'] == 'NOT_FOUND' and 'kitId' in error:
                errors.append(dterrors.ClaimErrorKitNotFound(error))
            else:
                errors.append(dterrors.ClaimError(error))
        return errors

    def _resolve_type(self, claim: dict) -> Claim.ClaimKit | Claim.ClaimDevice:
        """
        Return either Kit or Device depending on type.

        Parameters
        ----------
        claim : dict
            Unmodified claim response dictionary.

        Returns
        -------
        claim_item : Claim.ClaimKit | Claim.ClaimDevice
            Either a Kit or Device object depending on type.

        """

        if claim['type'] == Claim.KIT:
            return Claim.ClaimKit(claim['kit'])
        elif claim['type'] == Claim.DEVICE:
            return Claim.ClaimDevice(claim['device'])
        else:
            raise KeyError(f'unknown claim type {claim["type"]}')

    class ClaimDevice(dtoutputs.OutputBase):
        """
        Namespacing type for a claimed device.

        Attributes
        ----------
        device_id : str
            Unique device identifier.
        device_type : str
            :ref:`Device type <device_type_constants>`.
        product_number : str
            The device product number.
        is_claimed : bool
            Whether or not the devices has been claimed.

        """

        def __init__(self, device: dict) -> None:
            """
            Constructs the claimed Device object from raw response.

            """

            # Inherit from OutputBase parent.
            dtoutputs.OutputBase.__init__(self, device)

            # Unpack attributes from raw response dictionary.
            self.device_id: str = device['deviceId']
            self.device_type: str = device['deviceType']
            self.product_number: str = device['productNumber']
            self.is_claimed: bool = device['isClaimed']

    class ClaimKit(dtoutputs.OutputBase):
        """
        Namespacing type for a claimed kit.

        Attributes
        ----------
        kit_id : str
            Unique kit identifier.
        display_name : str
            Human reabable kit name.
        devices : list[Claim.ClaimDevice]
            List of devices in the kit.

        """

        def __init__(self, kit: dict) -> None:
            """
            Constructs the claimed kit object from raw response.

            """

            # Inherit from OutputBase parent.
            dtoutputs.OutputBase.__init__(self, kit)

            # Unpack attributes from raw response dictionary.
            self.kit_id: str = kit['kitId']
            self.display_name: str = kit['displayName']
            self.devices: List[Claim.ClaimDevice] \
                = [Claim.ClaimDevice(d) for d in kit['devices']]
