#!/usr/bin/env python3
"""Build an OFFLINE X1P topology candidate; never install or activate it."""
import argparse, ctypes, shutil, struct, subprocess, json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
if a.output.exists() or a.output.resolve().is_relative_to('/boot'):p.error('Use a new output outside /boot.')
def get(node,prop,kind='x',file=None):
 return subprocess.check_output(['fdtget','-t',kind,str(file or a.output),node,prop],text=True).strip()
def put(*v):subprocess.run(['fdtput',*v],check=True)
shutil.copyfile(a.source,a.output)
assert get('/cpus/cpu@20200','reg')=='0 20200'
assert get('/cpus/cpu@20300','reg')=='0 20300'
# Preserve CPU node order and handles: the last two nodes become 20100/20200.
handles=[get('/cpus/cpu@'+n,'phandle') for n in ('20200','20300')]
for i,h in enumerate(handles,1):assert get('/cpus/cpu-map/cluster2/core'+str(i),'cpu')==h
library=ctypes.CDLL('libfdt.so.1');vp=ctypes.c_void_p;ci=ctypes.c_int;cp=ctypes.c_char_p
library.fdt_open_into.argtypes=[vp,vp,ci];library.fdt_path_offset.argtypes=[vp,cp];library.fdt_set_name.argtypes=[vp,ci,cp];library.fdt_pack.argtypes=[vp]
blob=a.output.read_bytes();original=ctypes.create_string_buffer(blob);buffer=ctypes.create_string_buffer(len(blob)+4096)
assert library.fdt_open_into(original,buffer,len(buffer))==0
for old,new in (('20200','20100'),('20300','20200')):
 offset=library.fdt_path_offset(buffer,('/cpus/cpu@'+old).encode());assert offset>=0
 assert library.fdt_set_name(buffer,offset,('cpu@'+new).encode())==0
assert library.fdt_pack(buffer)==0
a.output.write_bytes(buffer.raw[:struct.unpack_from('>I',buffer.raw,4)[0]])
for address,pd in (('20100','cpu_pd9'),('20200','cpu_pd10')):
 node='/cpus/cpu@'+address;power=get(node,'power-domains').split();path=get('/__symbols__',pd,'s')
 power[0]=get(path,'phandle')
 put('-t','x',str(a.output),node,'reg','0',address)
 put('-t','x',str(a.output),node,'power-domains',*power)
for name in subprocess.check_output(['fdtget','-p',str(a.output),'/__symbols__'],text=True).split():
 if get('/__symbols__',name,'s')=='/cpus/cpu@20300':put('-d',str(a.output),'/__symbols__',name)
put('-t','s',str(a.output),'/__symbols__','cpu9','/cpus/cpu@20100')
nodes=[n for n in subprocess.check_output(['fdtget','-l',str(a.output),'/cpus'],text=True).split() if n.startswith('cpu@')]
assert len(nodes)==10 and 'cpu@20300' not in nodes
assert nodes==sorted(nodes,key=lambda n:int(n.split('@')[1],16))
assert get('/cpus/cpu@20100','phandle')==handles[0]
assert get('/cpus/cpu@20200','phandle')==handles[1]
print(json.dumps({'candidate':str(a.output),'cpu_nodes':nodes,'status':'offline candidate only; not boot-tested on this unit'},indent=2))
