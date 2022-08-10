from __future__ import annotations

from typing import Any, Optional, List, Tuple

import disruptive.outputs as dtoutputs
import disruptive.requests as dtrequests
import disruptive.errors as dterrors


class Claim(dtoutputs.OutputBase):
    """
    Namespacing for claim methods.

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
        self.claimed_item: Claim.Kit | Claim.Device = self._resolve_type(claim)

    @classmethod
    def claim_info(cls, identifier: str, **kwargs: Any) -> Claim:
        """
        Get the claim information for either a kit or device.
        The identifier can be found in the sensor QR code or
        as an xid printed directly on the sensor.

        Parameters
        ----------
        identifier : str
            Unique ID of the target Device or Kit.

        Returns
        -------
        claim : Device | Kit
            Claim information about the requested Device or Kit.

        Raises
        ------
        TypeError
            If provided identifier is not str type.

        """

        if not isinstance(identifier, str):
            raise TypeError(f'Identifier must be str, got {type(identifier)}.')

        url = f':claim-info?identifier={identifier}'

        return cls(dtrequests.DTRequest.get(url, **kwargs))

    @staticmethod
    def claim(project_id: str,
              kit_ids: Optional[List[str]] = None,
              device_ids: Optional[List[str]] = None,
              dry_run: bool = False,
              **kwargs: Any,
              ) -> Tuple[List[Claim.Device], List[Exception]]:
        """
        Claim a number of kits and/or devices to your project.

        Parameters
        ----------
        project_id : str
            Unique identifier of target project.
        kit_ids : list[str], optional
            List of unique kit IDs to claim.
        device_ids : list[str], optional
            List of unique device IDs to claim.
        dry_run : bool, optional
            Test your claim request during development.
            No kits or devices will be claimed.
        **kwargs
            Arbitrary keyword arguments.
            See the :ref:`Configuration <configuration>` page.

        Returns
        -------
        devices : list[Claim.Device]
            List of successfully claimed devices.
        errors : list[ClaimError]
            List of errors that occured during claiming.
            If list is empty, all devices were claimed successfully.

        """

        url = f'/projects/{project_id}/devices:claim'
        url += f'?dryRun={str(dry_run).lower()}'

        body = {}
        if kit_ids is not None:
            body['kitIds'] = kit_ids
        if device_ids is not None:
            body['deviceIds'] = device_ids

        res = dtrequests.DTRequest.post(url, body=body, **kwargs)

        return (
            [Claim.Device(d) for d in res['claimedDevices']],
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

    def _resolve_type(self, claim: dict) -> Claim.Kit | Claim.Device:
        """
        Return either Kit or Device depending on type.

        Parameters
        ----------
        claim : dict
            Unmodified claim response dictionary.

        Returns
        -------
        claim_item : Claim.Kit | Claim.Device
            Either a Kit or Device object depending on type.

        """

        if claim['type'] == Claim.KIT:
            return Claim.Kit(claim['kit'])
        elif claim['type'] == Claim.DEVICE:
            return Claim.Device(claim['device'])
        else:
            raise KeyError(f'unknown claim type {claim["type"]}')

    class Device(dtoutputs.OutputBase):
        """
        Namespacing type for a claimed device.

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

    class Kit(dtoutputs.OutputBase):
        """
        Namespacing type for a claimed kit.

        """

        def __init__(self, kit: dict) -> None:
            """
            Constructs the claimed Kit object from raw response.

            """

            # Inherit from OutputBase parent.
            dtoutputs.OutputBase.__init__(self, kit)

            # Unpack attributes from raw response dictionary.
            self.kit_id: str = kit['kitId']
            self.display_name: str = kit['displayName']
            self.devices: List[Claim.Device] \
                = [Claim.Device(d) for d in kit['devices']]
