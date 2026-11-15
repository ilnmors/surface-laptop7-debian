// SPDX-License-Identifier: GPL-2.0-or-later
#pragma once
#include <linux/input-event-codes.h>
#include <vector>
#include <string>
namespace iptsd::apps::daemon {
struct TestEvent { int type, code, value; };
class UinputDevice {
public:
 inline static std::vector<TestEvent> events;
 inline static int left = 0;
 void set_name(const std::string &) {} void set_vendor(int) {} void set_product(int) {}
 void set_evbit(int) {} void set_propbit(int) {} void set_keybit(int) {}
 void set_absinfo(int,int,int,int) {} void create() {}
 void emit(int type,int code,int value) const {
  events.push_back({type,code,value});
  if (type == EV_KEY && code == BTN_LEFT) left = value;
 }
};
}
