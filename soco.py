import xml.etree.cElementTree as XML

import requests

class SoCo(object):
    """A simple class for controlling a Sonos speaker.

    Public functions:
    play -- Plays the currently selected track or a music stream.
    pause -- Pause the currently playing track.
    stop -- Stop the currently playing track.
    next -- Go to the next track.
    previous -- Go back to the previous track.
    mute -- Mute (or unmute) the speaker.
    volume -- Get or set the volume of the speaker.
    bass -- Get or set the speaker's bass EQ.
    treble -- Set the speaker's treble EQ.
    set_loudness -- Turn on (or off) the speaker's loudness compensation.
    switch_to_line_in -- Switch the speaker's input to line-in.
    status_light -- Turn on (or off) the Sonos status light.
    get_current_track_info -- Get information about the currently playing track.
    get_speaker_info -- Get information about the Sonos speaker.

    """

    TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
    RENDERING_ENDPOINT = '/MediaRenderer/RenderingControl/Control'
    DEVICE_ENDPOINT = '/DeviceProperties/Control'
    MEDIA_SERVER_ENDPOINT = '/MediaServer/ContentDirectory/Control'

    speaker_info = {}

    def __init__(self, speaker_ip):
        self.speaker_ip = speaker_ip

    def play(self, uri=''):
        """Play the currently selected track or play a stream.

        Arguments:
        uri -- URI of a stream to be played.

        Returns:
        True if the Sonos speaker successfully started playing the track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.

        """
        if uri is not '':
            action = '"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"'

            body = '<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>' + uri + '</CurrentURI><CurrentURIMetaData></CurrentURIMetaData></u:SetAVTransportURI>'

            response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetAVTransportURIResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:SetAVTransportURIResponse></s:Body></s:Envelope>'):
                # The track is enqueued, now play it.
                return self.play()
            else:
                return self.__parse_error(response)

        else:
            action = '"urn:schemas-upnp-org:service:AVTransport:1#Play"'

            body = '<u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Play>'

            response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:PlayResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:PlayResponse></s:Body></s:Envelope>'):
                return True
            else:
                return self.__parse_error(response)

    def pause(self):
        """ Pause the currently playing track.

        Returns:
        True if the Sonos speaker successfully paused the track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Pause"'

        body = '<u:Pause xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Pause>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:PauseResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:PauseResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def stop(self):
        """ Stop the currently playing track.
        
        Returns:
        True if the Sonos speaker successfully stopped the playing track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Stop"'

        body = '<u:Stop xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Stop>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:StopResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:StopResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def next(self):
        """ Go to the next track.
        
        Returns:
        True if the Sonos speaker successfully skipped to the next track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned. Keep in mind that next() can return errors
        for a variety of reasons. For example, if the Sonos is streaming
        Pandora and you call next() several times in quick succession an error
        code will likely be returned (since Pandora has limits on how many
        songs can be skipped).
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Next"'

        body = '<u:Next xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Next>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:NextResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:NextResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def previous(self):
        """ Go back to the previously played track.
        
        Returns:
        True if the Sonos speaker successfully went to the previous track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned. Keep in mind that previous() can return errors
        for a variety of reasons. For example, previous() will return an error
        code (error code 701) if the Sonos is streaming Pandora since you can't
        go back on tracks.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Previous"'

        body = '<u:Previous xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Previous>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:PreviousResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:PreviousResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def mute(self, mute):
        """ Mute or unmute the Sonos speaker.

        Arguments:
        mute -- True to mute. False to unmute.
        
        Returns:
        True if the Sonos speaker was successfully muted or unmuted.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if mute is True:
            mute_value = '1'
        else:
            mute_value = '0'

        action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetMute"'

        body = '<u:SetMute xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel><DesiredMute>' + mute_value + '</DesiredMute></u:SetMute>'

        response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetMuteResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetMuteResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.parse(response)



    def start_playlist(self, nr=''):
        """start a playlist

        Arguments:

        Returns:

        """

        # temporary
        nr = str(1)

        if nr is '':
            action = ''
        else:
            action = '"urn:schemas-upnp-org:service:AVTransport:1#StartAutoplay"'

            body = '<u:StartAutoplay xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><ProgramURI>file:///jffs/settings/savedqueues.rsq#0</ProgramURI><ProgramMetaData>DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upup="urn:schemas-upnp.org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" itemid="SD:0" parentID="SD"></ProgramMetaData><Volume>8</Volume><IncludeLinkedZones>0</IncludeLinkedZones><ResetVolumeAfter>1</ResetVolumeAfter></u:StartAutoplay>'

            # <ProgramURI>file:///jffs/settings/savedqueues.rsq#0</ProgramURI><ProgramMetaData>DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:upup="urn:schemas-upnp.org:metadata-1-0/upnp/" xmlns:r="urn:schemas-rinconnetworks-com:metadata-1-0/" xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/" itemid="SD:0" parentID="SD"></ProgramMetaData>

            response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:StartAutoplayResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:StartAutoplayResponse></s:Body></s:Envelope>'):
                return True
            else:
                return self.__parse_error(response)

    # def start_playlist(self, nr=''):
    #     """start a playlist

    #     Arguments:

    #     Returns:

    #     """
    #     # temporary
    #     nr = str(1)

    #     if nr is '':
    #         action = ''
    #     else:
    #         action = '"urn:schemas-upnp-org:service:ContentDirectory:1#Browse"'

    #         body = '<u:Browse xmlns:u="urn:schemas-upnp-org:service:ContentDirectory:1"><ObjectID>SQ:1</ObjectID><BrowseFlag>BrowseDirectChildren</BrowseFlag><Filter></Filter><StartingIndex>0</StartingIndex><RequestedCount>1000</RequestedCount><SortCriteria></SortCriteria></u:Browse>'

    #         print body

    #         response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

    #         print response

    #         if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:BrowseResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:BrowseResponse></s:Body></s:Envelope>'):
    #             return True
    #         else:
    #             return self.__parse_error(response)











    # Utility functions  

    def set_playmode(self, play_mode=''):
        """start a playlist

        Arguments:

        Returns:

        """

        # temporary
        play_mode = 'REPEAT_ALL'

        if play_mode is '':
            action = ''
        else:
            action = '"urn:schemas-upnp-org:service:AVTransport:1#SetPlayMode"'

            body = '<u:SetPlayMode xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><NewPlayMode>REPEAT_ALL</NewPlayMode></u:SetPlayMode>'

            response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetPlayModeResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:SetPlayModeResponse></s:Body></s:Envelope>'):
                return True
            else:
                return self.__parse_error(response)


    def volume(self, volume=False):
        """ Get or set the Sonos speaker volume.

        Arguments:
        volume -- A value between 0 and 100.
        
        Returns:
        If the volume argument was specified: returns true if the Sonos speaker
        successfully set the volume.

        If the volume argument was not specified: returns the current volume of
        the Sonos speaker.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if volume:
            action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetVolume"'

            body = '<u:SetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel><DesiredVolume>' + repr(volume) + '</DesiredVolume></u:SetVolume>'

            response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetVolumeResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetVolumeResponse></s:Body></s:Envelope>'):
                return True
            else:
                return self.__parse_error(response)
        else:
            action = '"urn:schemas-upnp-org:service:RenderingControl:1#GetVolume"'

            body = '<u:GetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel></u:GetVolume>'

            response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

            dom = XML.fromstring(response)

            volume = dom.findtext('.//CurrentVolume')

            return int(volume)

    def bass(self, bass=''):
        """ Get or set the Sonos speaker's bass EQ.

        Arguments:
        bass -- A value between -10 and 10.
        
        Returns:
        If the bass argument was specified: returns true if the Sonos speaker
        successfully set the bass EQ.

        If the bass argument was not specified: returns the current base value.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if bass != '':
            action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetBass"'

            body = '<u:SetBass xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><DesiredBass>' + repr(bass) + '</DesiredBass></u:SetBass>'

            response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetBassResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetBassResponse></s:Body></s:Envelope>'):
                return True
            else:
                return self.__parse_error(response)
        else:
            action = '"urn:schemas-upnp-org:service:RenderingControl:1#GetBass"'

            body = '<u:GetBass xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel></u:GetBass>'

            response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

            dom = XML.fromstring(response)

            bass = dom.findtext('.//CurrentBass')

            return int(bass)

    def treble(self, treble=False):
        """ Get or set the Sonos speaker's treble EQ.

        Arguments:
        treble -- A value between -10 and 10.
        
        Returns:
        If the treble argument was specified: returns true if the Sonos speaker
        successfully set the treble EQ.

        If the treble argument was not specified: returns the current treble value.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if treble:
            action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetTreble"'

            body = '<u:SetTreble xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><DesiredTreble>' + repr(treble) + '</DesiredTreble></u:SetTreble>'

            response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

            if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetTrebleResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetTrebleResponse></s:Body></s:Envelope>'):
                return True
            else:
                return self.__parse_error(response)
        else:
            action = '"urn:schemas-upnp-org:service:RenderingControl:1#GetTreble"'

            body = '<u:GetTreble xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel></u:GetTreble>'

            response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

            dom = XML.fromstring(response)

            treble = dom.findtext('.//CurrentTreble')

            return int(treble)

    def set_loudness(self, loudness):
        """ Set the Sonos speaker's loudness compensation.

        Loudness is a complicated topic. You can find a nice summary about this
        feature here: http://forums.sonos.com/showthread.php?p=4698#post4698

        Arguments:
        loudness -- True to turn on loudness compensation. False to disable it.
        
        Returns:
        True if the Sonos speaker successfully set the loundess compensation. 
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetLoudness"'

        if loudness is True:
            loudness_value = '1'
        else:
            loudness_value = '0'

        body = '<u:SetLoudness xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel><DesiredLoudness>' + loudness_value + '</DesiredLoudness></u:SetLoudness>'

        response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetLoudnessResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetLoudnessResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def switch_to_line_in(self):
        """ Switch the speaker's input to line-in.

        Returns:
        True if the Sonos speaker successfully switched to line-in.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned. Note, an error will be returned if you try
        to switch to line-in on a device (like the Play:3) that doesn't have
        line-in capability.

        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"'

        speaker_info = self.get_speaker_info()

        body = '<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>x-rincon-stream:' + speaker_info['uid'] + '</CurrentURI><CurrentURIMetaData></CurrentURIMetaData></u:SetAVTransportURI>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetAVTransportURIResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:SetAVTransportURIResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def status_light(self, led_on):
        """ Turn on (or off) the white Sonos status light.

        Turns on or off the little white light on the Sonos speaker. (It's
        between the mute button and the volume up button on the speaker.)

        Arguments:
        led_on -- True to turn on the light. False to turn off the light.
        
        Returns:
        True if the Sonos speaker successfully turned on (or off) the light.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if led_on is True:
            led_state = 'On'
        else:
            led_state = 'Off'

        action = '"urn:schemas-upnp-org:service:DeviceProperties:1#SetLEDState"'

        body = '<u:SetLEDState xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1"><DesiredLEDState>' + led_state + '</DesiredLEDState>'

        response = self.__send_command(SoCo.DEVICE_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetLEDStateResponse xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1"></u:SetLEDStateResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.parse(response)

    def get_current_track_info(self):
        """ Get information about the currently playing track.
        
        Returns:
        A dictionary containing the following information about the currently
        playing track: playlist_position, duration, title, artist, album, and
        a link to the album art.
        
        If we're unable to return data for a field, we'll return an empty
        string. This can happen for all kinds of reasons so be sure to check
        values. For example, a track may not have complete metadata and be
        missing an album name. In this case track['album'] will be an empty string.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo"'

        body = '<u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Channel>Master</Channel></u:GetPositionInfo>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        dom = XML.fromstring(response)

        track = {}

        track['playlist_position'] = dom.findtext('.//Track')
        track['duration'] = dom.findtext('.//TrackDuration')
        track['uri'] = dom.findtext('.//TrackURI')

        d = dom.findtext('.//TrackMetaData')

        # If the speaker is playing from the line-in source, querying for track
        # metadata will return "NOT_IMPLEMENTED".
        if d is not '' or d is not 'NOT_IMPLEMENTED':
            # Track metadata is returned in DIDL-Lite format
            metadata = XML.fromstring(d.encode('utf-8'))

            track['title'] = metadata.findtext('.//{http://purl.org/dc/elements/1.1/}title')
            track['artist'] = metadata.findtext('.//{http://purl.org/dc/elements/1.1/}creator')
            track['album'] = metadata.findtext('.//{urn:schemas-upnp-org:metadata-1-0/upnp/}album')

            album_art = metadata.findtext('.//{urn:schemas-upnp-org:metadata-1-0/upnp/}albumArtURI')

            if album_art is not None:
                track['album_art'] = 'http://' + self.speaker_ip + ':1400' + metadata.findtext('.//{urn:schemas-upnp-org:metadata-1-0/upnp/}albumArtURI')
            else:
                track['album_art'] = ''
        else:
            track['title'] = ''
            track['artist'] = ''
            track['album'] = ''
            track['album_art'] = ''

        return track

    def get_speaker_info(self, refresh=False):
        """ Get information about the Sonos speaker.

        Arguments:
        refresh -- Refresh the speaker info cache.

        Returns:
        Information about the Sonos speaker, such as the UID, MAC Address, and
        Zone Name.

        """
        if self.speaker_info and refresh is False:
            return self.speaker_info
        else:
            response = requests.get('http://' + self.speaker_ip + ':1400/status/zp')

            dom = XML.fromstring(response.content)

            self.speaker_info['zone_name'] = dom.findtext('.//ZoneName')
            self.speaker_info['zone_icon'] = dom.findtext('.//ZoneIcon')
            self.speaker_info['uid'] = dom.findtext('.//LocalUID')
            self.speaker_info['serial_number'] = dom.findtext('.//SerialNumber')
            self.speaker_info['software_version'] = dom.findtext('.//SoftwareVersion')
            self.speaker_info['hardware_version'] = dom.findtext('.//HardwareVersion')
            self.speaker_info['mac_address'] = dom.findtext('.//MACAddress')

            return self.speaker_info

    def __send_command(self, endpoint, action, body):
        """ Send a raw command to the Sonos speaker.

        Returns:
        The raw response body returned by the Sonos speaker.

        """
        headers = {
            'Content-Type': 'text/xml',
            'SOAPACTION': action
        }

        soap = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>' + body + '</s:Body></s:Envelope>'

        r = requests.post('http://' + self.speaker_ip + ':1400' + endpoint, data=soap, headers=headers)

        return r.content

    def __parse_error(self, response):
        """ Parse an error returned from the Sonos speaker.

        Returns:
        The UPnP error code returned by the Sonos speaker.

        If we're unable to parse the error response for whatever reason, the
        raw response sent back from the Sonos speaker will be returned.
        """
        error = XML.fromstring(response)

        errorCode = error.findtext('.//{urn:schemas-upnp-org:control-1-0}errorCode')

        if errorCode is not None:
            return int(errorCode)
        else:
            # Unknown error, so just return the entire response
            return response
