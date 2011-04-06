# -*- coding: utf-8 -*-

import tempfile
import urllib2
from redturtle.video.metadataextractor import extract

def _setVideoMetadata(object, name):
    """Set the metadata taken from the video using hachoir
    """
    metadata = extract(name)
    if metadata is not None:
        # duration
        try:
            duration = metadata.getItems('duration')
        except ValueError:
            # no valid data
            return
        if len(duration) >= 1:
            strdate=str(duration[0].value)
            strdate=strdate.split('.')
            strdate=strdate[0]
            object.setDuration(strdate)
        # size
        try:
            width = metadata.getItems('width')[0].value
            height = metadata.getItems('height')[0].value
        except ValueError:
            # no valid data
            return
        object.setWidth(width)
        object.setHeight(height)


def createTempFileInternalVideo(object, event):
    """Create a temporary file for InternalVideo
    """
    if object.getDuration():
        return
    file=object.getFile()
    fd=tempfile.NamedTemporaryFile()
    if type(file.data)==str:
        # blob support
        fd.write(file.data)
    else:
        # No blob
        fd.write(file.data.data)
    _setVideoMetadata(object, fd.name)
    object.reindexObject()
    fd.close()


def createTempFileRemoteVideo(object, event):
    """Create a temporary file for RemoteVideo
    """
    if object.getDuration():
        return
    url=object.getRemoteUrl()
    response = urllib2.urlopen(url)
    fd=tempfile.NamedTemporaryFile()
    fd.write(response.read())
    _setVideoMetadata(object, fd.name)
    object.reindexObject()
    fd.close()
