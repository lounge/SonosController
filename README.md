# Sonos Controller (sonos-cli)
## Introduction
Sonos Controller is a command line interface (cli) to interface with the SONOS speakers with a shell

## Sample
*Note: For these examples we'll assume that the Sonos speaker IP is `192.168.1.162`*  

The shell provides an immediate way to configure your SONOS speakers,
for example, to set the volume to 60% one can issue this simple command

`./sonoshell 192.168.1.162 volume 60`

### Play
If you already have something in your play queue you could simply issue:  
```bash
./sonoshell 192.168.1.162 play https://app.box.com/shared/static/lhtefwqwo6070tj8g5cq.mp3
```
where obviously `https://app.box.com/shared/static/lhtefwqwo6070tj8g5cq.mp3` is your file URL

#### Radio  
In order to play a streamable URL it must me prepended with some protocol specifications,
for BBC Radio 1 is the `hls-radio://`  

Here is an example:  
```bash
./sonoshell 192.168.1.162 play hls-radio://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/hls/nonuk/sbr_low/ak/bbc_radio_one.m3u8
```

Some other protocol includes:
```
x-rincon-mp3radio://
aac://
```

Here is another working example (The URL is from the Swiss RSI Rete Tre radio, it's an m3u stream):  
```bash
./sonoshell 192.168.1.162 play x-rincon-mp3radio://stream.srg-ssr.ch/retetre/aacp_96.m3u
```

### EQ
Another good example is setting the EQ:  
to do so you have to send the following commands

####Bass  
```bash
./sonoshell 192.168.1.162 eq bass 3
```

####Treble  
```bash
./sonoshell 192.168.1.162 eq treble 3
```

*Note: Eq values go from -10 to 10, and the Middle couldn't be set (due to a Sonos limitation)*

### LED  
The Sonos speakers have an LED placed over them. To activate / deactivate it you can simply send the following command
#### Deactivate
```bash
./sonoshell 192.168.1.162 led 0
```

#### Activate
```
./sonoshell 192.168.1.162 led 1
```

## Available commands

### play [url]
Plays the current song or the one specified by the URL  
### pause
Pause the sound reproduction  
### volume [0-100]
Passing the command without a parameter will return the current volume, otherwise it will set it to the one specified  
### eq bass|treble [-10 - 10]
Get / Set the equalizer, see the [Sample](#Sample) above  
### led 0|1
Set the LED status  
### next
Play the next song in queue  
### previous  
Play the previous song in queue  
### info
Get information about the current playing song  