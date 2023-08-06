
all: run

UDEVPATH=$(shell pkg-config  udev --variable udevdir)/rules.d/
UDEVFN=41-nitrokey.rules
UDEV=$(UDEVPATH)/$(UDEVFN)
UDEVLINK=https://github.com/Nitrokey/libnitrokey/blob/master/data/41-nitrokey.rules
$(UDEV):
	wget $(UDEVLINK) -O /tmp/$(UDEVFN)
	sudo cp /tmp/$(UDEVFN) $@
	sudo udevadm control --reload-rules
	sudo udevadm trigger

.PHONY: setup
setup: $(UDEV)
	# sudo needed for dfu bootloader access, can be solved with udev rules instead
	pipenv --python 3.9
	# libusb1 intelhex
	pipenv install flit
	pipenv run flit install -s

.PHONY: clean
clean:
	pipenv --rm


FWREL=../release/nitrokey-pro-firmware-v0.14-RC2-to_update.bin
FW=$(shell readlink -f $(FWREL))
PIDVID=20a0:42b4

.PHONY: run
run:
	# sudo needed for dfu bootloader access, can be solved with udev rules?
	sudo pipenv run nkdfu -f $(FW)

WORKSPACE=~/work
DFUP=$(WORKSPACE)/nitrokey-pro-firmware/build/gcc
DFU=cd $(DFUP) && make -f dfu.mk

.PHONY: compare
compare:
	-rm original.hex python.hex
	# 1. dfu-util tool
	$(DFU) flash-bootloader
	$(DFU) flash-dfu FIRMWAREBIN=$(shell readlink -f $(FW))
	$(DFU) download-image DOWNLOAD=original.hex
	# 2. python-dfu tool
	$(DFU) flash-bootloader
	sleep 2s
	-$(MAKE) run
	echo !!! Reset/reconnection is required to download the new content from the flash
	-STM32_Programmer_CLI -c port=SWD -halt  -rst
	$(DFU) download-image DOWNLOAD=python.hex

	mv $(DFUP)/{original.hex,python.hex} .
	hexdiff.py original.hex python.hex | colordiff | less -R

.PHONY: run-update-cycle
run-update-cycle:
	$(DFU) flash-bootloader
	sleep 1s
	$(MAKE) run
	sleep 1s
	-#STM32_Programmer_CLI -c port=SWD -halt  -rst
