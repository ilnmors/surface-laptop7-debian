#!/bin/bash
# Disable the unused x8 PCIe3 controller (no endpoint on Romulus13) in the verified Surface DTB.
set -euo pipefail
here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
in=${1:-$here/base.dtb}; out=${2:-$here/surface-sl7-xplus-pcie3-off.dtb}
cp "$in" "$out"
fdtput -t s "$out" /soc@0/pcie@1bd0000 status disabled
# The PHY stays enabled: GCC lists its pipe clock as a clock input, and an unused PHY stays powered off.
[[ $(fdtget -t s "$out" /soc@0/pcie@1bd0000 status) == disabled ]]
echo "$out"
