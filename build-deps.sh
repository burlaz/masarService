#!/bin/sh
set -e -x

CURDIR="$PWD"

cat << EOF > configure/RELEASE.local
EPICS_BASE=$HOME/.source/epics-base
PVDATA=$HOME/.source/pvDataCPP
PVACCESS=$HOME/.source/pvAccessCPP
EOF
cat configure/RELEASE.local

install -d "$HOME/.source"
cd "$HOME/.source"

git clone --quiet --depth 5 --branch "$BRBASE" https://github.com/epics-base/epics-base.git epics-base
git clone --quiet --depth 5 --branch "$BRPVD" https://github.com/epics-base/pvDataCPP.git pvDataCPP
git clone --quiet --depth 5 --branch "$BRPVA" https://github.com/epics-base/pvAccessCPP.git pvAccessCPP
git clone --quiet --depth 5                   https://github.com/mdavidsaver/p4p.git p4p

(cd epics-base && git log -n1 )
(cd pvDataCPP && git log -n1 )
(cd pvAccessCPP && git log -n1 )
(cd p4p && git log -n1 )

EPICS_HOST_ARCH=`sh epics-base/startup/EpicsHostArch`

case "$CMPLR" in
clang)
  echo "Host compiler is clang"
  cat << EOF >> epics-base/configure/os/CONFIG_SITE.Common.$EPICS_HOST_ARCH
GNU         = NO
CMPLR_CLASS = clang
CC          = clang
CCC         = clang++
EOF

  # hack
  sed -i -e 's/CMPLR_CLASS = gcc/CMPLR_CLASS = clang/' epics-base/configure/CONFIG.gnuCommon

  clang --version
  ;;
*)
  echo "Host compiler is default"
  gcc --version
  ;;
esac

(cd epics-base && git log -n1 )
(cd pvDataCPP && git log -n1 )
(cd pvAccessCPP && git log -n1 )

EPICS_HOST_ARCH=`sh epics-base/startup/EpicsHostArch`

case "$CMPLR" in
clang)
  echo "Host compiler is clang"
  cat << EOF >> epics-base/configure/os/CONFIG_SITE.Common.$EPICS_HOST_ARCH
GNU         = NO
CMPLR_CLASS = clang
CC          = clang
CCC         = clang++
EOF

  # hack
  sed -i -e 's/CMPLR_CLASS = gcc/CMPLR_CLASS = clang/' epics-base/configure/CONFIG.gnuCommon

  clang --version
  ;;
*)
  echo "Host compiler is default"
  gcc --version
  ;;
esac

cat << EOF > pvDataCPP/configure/RELEASE.local
EPICS_BASE=$HOME/.source/epics-base
EOF

cat << EOF > pvAccessCPP/configure/RELEASE.local
PVDATA=$HOME/.source/pvDataCPP
EPICS_BASE=$HOME/.source/epics-base
EOF

cat << EOF > p4p/configure/RELEASE.local
PVACCESS=$HOME/.source/pvAccessCPP
PVDATA=$HOME/.source/pvDataCPP
EPICS_BASE=$HOME/.source/epics-base
EOF

make -j2 -C epics-base
make -j2 -C pvDataCPP
make -j2 -C pvAccessCPP
make -j2 -C p4p "$@"

ls -d p4p/python*
