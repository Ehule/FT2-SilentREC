#pragma once

#ifdef HAS_MIDI

#include <stdint.h>
#include <stdbool.h>
#include <SDL2/SDL.h>

#define MIDI_INPUT_SELECTOR_BOX_WIDTH 247
#define MAX_MIDI_DEVICES 99

typedef struct midi_t
{
	char *inputDeviceName, *inputDeviceNames[MAX_MIDI_DEVICES];
	volatile bool initThreadDone, callbackBusy, enable;
	bool dubEnable;
	bool rescanDevicesFlag;
	uint32_t inputDevice, numInputDevices;
	int16_t currMIDIVibDepth, currMIDIPitch;
	SDL_Thread *initMidiThread;
} midi_t;

extern midi_t midi; // ft2_midi.c

void closeMidiInDevice(void);
void freeMidiIn(void);
void freeMidiOut(void);
bool initMidiIn(void);
bool openMidiInDevice(uint32_t deviceID);
void recordMIDIEffect(uint8_t efx, uint8_t efxData);
void midiDubNoteOn(uint8_t channelIndex, uint8_t note, uint8_t velocity);
void midiDubNoteOff(uint8_t channelIndex);
void midiDubPanic(void);
bool saveMidiInputDeviceToConfig(void);
bool setMidiInputDeviceFromConfig(void);
void freeMidiInputDeviceList(void);
void rescanMidiInputDevices(void);
void drawMidiInputList(void);
void scrollMidiInputDevListUp(void);
void scrollMidiInputDevListDown(void);
void sbMidiInputSetPos(uint32_t pos);
bool testMidiInputDeviceListMouseDown(void);
int32_t initMidiFunc(void *ptr);

#endif
