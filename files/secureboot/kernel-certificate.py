#!/usr/bin/python3
"""Insert a DER certificate in Linux's CONFIG_SYSTEM_EXTRA_CERTIFICATE reserve."""
from pathlib import Path
import gzip
import struct
import subprocess


def certificates(data):
    result=[]
    position=0
    while position<len(data):
        if data[position]!=0x30:
            raise ValueError('Invalid certificate list entry')
        size=data[position+1]
        header=2
        if size&0x80:
            count=size&0x7f
            if not 1<=count<=4:
                raise ValueError('Invalid certificate length')
            size=int.from_bytes(data[position+2:position+2+count],'big')
            header+=count
        end=position+header+size
        if end>len(data):
            raise ValueError('Truncated certificate list')
        result.append(data[position:end])
        position=end
    return result


def insert_certificate(payload, kernel, certificate):
    if payload[4:8]==b'zimg':
        offset,size=struct.unpack_from('<II',payload,8)
        kind=payload[24:56].split(b'\0')[0]
        compressed=payload[offset:offset+size]
        if kind==b'zstd':
            payload=subprocess.check_output(['zstd','-dc'],input=compressed)
        elif kind==b'gzip':
            payload=gzip.decompress(compressed)
        else:
            raise ValueError('Unsupported EFI zboot compression')
    if payload[56:60]!=b'ARM\x64':
        raise ValueError('Expected an ARM64 Image')
    symbols={}
    required={'_text','system_certificate_list','system_extra_cert',
              'system_extra_cert_used','system_certificate_list_size'}
    for line in Path('/boot/System.map-'+kernel).read_text().splitlines():
        parts=line.split()
        if len(parts)==3 and parts[2] in required:
            symbols[parts[2]]=int(parts[0],16)
    if symbols.keys()!=required:
        raise ValueError('Missing kernel certificate symbols')
    config=Path('/boot/config-'+kernel).read_text().splitlines()
    if 'CONFIG_SYSTEM_EXTRA_CERTIFICATE=y' not in config:
        raise ValueError('Kernel has no reserved certificate support')
    capacity=int(next(s.split('=',1)[1] for s in config if s.startswith('CONFIG_SYSTEM_EXTRA_CERTIFICATE_SIZE=')))
    base=symbols['_text']
    start=symbols['system_certificate_list']-base
    extra=symbols['system_extra_cert']-base
    used_offset=symbols['system_extra_cert_used']-base
    size_offset=symbols['system_certificate_list_size']-base
    if not (0<start<extra and extra+capacity<=used_offset<size_offset and size_offset+8<=len(payload)):
        raise ValueError('Certificate symbols do not match Image layout')
    used=struct.unpack_from('<I',payload,used_offset)[0]
    list_size=struct.unpack_from('<Q',payload,size_offset)[0]
    if used>capacity or list_size!=extra-start+used:
        raise ValueError('Certificate list layout mismatch')
    original=certificates(payload[start:extra])
    if len(certificates(certificate))!=1 or len(certificate)>capacity:
        raise ValueError('Invalid or oversized extra certificate')
    output=bytearray(payload)
    output[extra:extra+capacity]=certificate+bytes(capacity-len(certificate))
    struct.pack_into('<I',output,used_offset,len(certificate))
    struct.pack_into('<Q',output,size_offset,list_size-used+len(certificate))
    assert certificates(output[start:extra+len(certificate)])==original+[certificate]
    # No instructions, drivers, or existing CA certificates may change.
    allowed=[(extra,extra+capacity),(used_offset,used_offset+4),(size_offset,size_offset+8)]
    previous=0
    for begin,end in allowed:
        assert output[previous:begin]==payload[previous:begin]
        previous=end
    assert output[previous:]==payload[previous:]
    return bytes(output)
