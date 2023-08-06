import logging

from pymobiledevice3.exceptions import PyMobileDevice3Exception, NotMountedError, UnsupportedCommandError
from pymobiledevice3.lockdown import LockdownClient


class MobileImageMounterService(object):
    SERVICE_NAME = 'com.apple.mobile.mobile_image_mounter'

    def __init__(self, lockdown: LockdownClient):
        self.logger = logging.getLogger(__name__)
        self.lockdown = lockdown
        self.service = self.lockdown.start_service(self.SERVICE_NAME)

    def list_images(self):
        """ Lookup mounted image by its name. """
        self.service.send_plist({'Command': 'CopyDevices'})
        response = self.service.recv_plist()

        if response.get('Error'):
            raise PyMobileDevice3Exception('unsupported command')

        return response

    def lookup_image(self, image_type):
        """ Lookup mounted image by its name. """
        self.service.send_plist({'Command': 'LookupImage',
                                 'ImageType': image_type})

        return self.service.recv_plist()

    def umount(self, image_type, mount_path, signature):
        """ umount image. """
        self.service.send_plist({'Command': 'UnmountImage',
                                 'ImageType': image_type,
                                 'MountPath': mount_path,
                                 'ImageSignature': signature})
        response = self.service.recv_plist()
        error = response.get('Error')
        if error:
            if error == 'UnknownCommand':
                raise UnsupportedCommandError()
            else:
                raise NotMountedError()

    def mount(self, image_type, signature):
        """ Upload image into device. """
        self.service.send_plist({'Command': 'MountImage',
                                 'ImageType': image_type,
                                 'ImageSignature': signature})
        result = self.service.recv_plist()
        status = result.get('Status')

        if status != 'Complete':
            raise PyMobileDevice3Exception(f'command MountImage failed with: {result}')

    def upload_image(self, image_type, image, signature):
        """ Upload image into device. """
        self.service.send_plist({'Command': 'ReceiveBytes',
                                 'ImageType': image_type,
                                 'ImageSize': len(image),
                                 'ImageSignature': signature})
        result = self.service.recv_plist()

        status = result.get('Status')

        if status != 'ReceiveBytesAck':
            raise PyMobileDevice3Exception(f'command ReceiveBytes failed with: {result}')

        self.service.sendall(image)
        result = self.service.recv_plist()

        status = result.get('Status')

        if status != 'Complete':
            raise PyMobileDevice3Exception(f'command ReceiveBytes failed to send bytes with: {result}')
