// SPDX-License-Identifier: GPL-2.0-or-later
#include "touch.hpp"
#include <iostream>
#include <thread>
using namespace iptsd;
using apps::daemon::TouchDevice;
using apps::daemon::UinputDevice;
using Contact = contacts::Contact<f64>;
static int failed = 0;
static void check(bool ok, const char *name) {
 std::cout << (ok ? "PASS " : "FAIL ") << name << "\n";
 if (!ok) ++failed;
}
static core::DeviceInfo device(u16 product = 0x0c77) {
 core::DeviceInfo d; d.vendor=0x045e; d.product=product; d.type=ipts::Device::Type::Touchpad; return d;
}
static Contact contact(usize id, bool stable=true, bool valid=true) {
 Contact c; c.index=id; c.mean={0.4+0.1*id,0.4}; c.size={0.06,0.04};
 c.valid=valid; c.stable=stable; c.normalized=true; return c;
}
static void frame(TouchDevice &d, std::initializer_list<Contact> c) {
 Image<f64> h=Image<f64>::Zero(18,26); d.update(std::vector<Contact>(c),h);
}
static void press(TouchDevice &d, bool active) {
 ipts::samples::Button b; b.active=active; b.pressure=active?1.0:0.0; d.update(b);
}
int main() {
 core::Config cfg; cfg.width=12; cfg.height=8;
 // Keep the actual default 25ms debounce; allow intentional state changes time.
 auto pause=[] { std::this_thread::sleep_for(std::chrono::milliseconds(30)); };
 {
  UinputDevice::left=0; TouchDevice d(cfg,device()); frame(d,{contact(0)}); press(d,true);
  frame(d,{contact(0,false)}); check(UinputDevice::left==1,"one-finger unstable fit retains physical click");
  frame(d,{contact(0)}); press(d,true); check(UinputDevice::left==1,"repeated held-button sample stays consistent");
  pause(); press(d,false); check(UinputDevice::left==0,"physical release ends drag");
 }
 {
  UinputDevice::left=0; TouchDevice d(cfg,device()); frame(d,{contact(0)}); press(d,true);
  frame(d,{contact(0,true,false),contact(1)}); frame(d,{contact(1)});
  check(UinputDevice::left==1,"two-finger contact handover retains physical click");
  auto c=contact(1); c.mean.x()=0.7; const auto first=UinputDevice::events.size(); frame(d,{c});
  bool moved=false; for(auto i=first;i<UinputDevice::events.size();++i)
   if(UinputDevice::events[i].type==EV_ABS && UinputDevice::events[i].code==ABS_MT_POSITION_X && UinputDevice::events[i].value==6720) moved=true;
  check(moved && UinputDevice::left==1,"remaining finger moves while click is held");
  pause();press(d,false);check(UinputDevice::left==0,"two-finger drag releases normally");
 }
 {
  UinputDevice::left=0; TouchDevice d(cfg,device()); frame(d,{contact(0)}); press(d,true); frame(d,{});
  check(UinputDevice::left==1,"empty contact frame does not invent button release");
  pause();press(d,false);check(UinputDevice::left==0,"raw release works after contact loss");
 }
 {
  UinputDevice::left=0; TouchDevice d(cfg,device()); frame(d,{contact(0)});press(d,true);d.disable();
  check(UinputDevice::left==0,"disable forcibly releases click");d.enable();frame(d,{contact(0)});press(d,true);
  check(UinputDevice::left==1,"enable does not retain stale debounce state");
 }
 {
  auto palm=cfg;palm.touchpad_disable_on_palm=true;UinputDevice::left=0;TouchDevice d(palm,device());
  frame(d,{contact(0)});press(d,true);frame(d,{contact(0,true,false)});press(d,true);
  check(UinputDevice::left==0,"palm suppression releases and blocks click");
  frame(d,{contact(0)});press(d,true);check(UinputDevice::left==1,"unblocked physical press can recover");
 }
 {
  UinputDevice::left=0;TouchDevice d(cfg,device(0x0c46));frame(d,{contact(0)});press(d,true);frame(d,{contact(0,false)});
  check(UinputDevice::left==0,"unrelated device legacy behavior unchanged");
 }
 std::cout << "Failures: " << failed << "\n";return failed?1:0;
}
