import functools
from src.common.midi_event import MidiEvent
from src.communication.messages import Message, MessageType, PlayingState, TempoModeMessage, TempoModeMessageType
from src.output_queue.output_comm import OutputCommSystem
from src.output_queue.playing_mode import PlayingMode

class TempoMode(PlayingMode):

    def __init__(self, output_queue):
        self.output_queue = output_queue
        self.comm_system = OutputCommSystem()

        self.playing_missed_notes = []
        self.playing_hit_notes = []

    def update(self, immediate_events: list, button_events: list, relative_time: float):
        for event in immediate_events:
            self.on_note_output(event)

        got_button_press = False
        for event in button_events:
            if event.event.type == "note_on":
                got_button_press = True

        # This mode only cares if a button was pressed, meaning they should't get played
        button_events.clear()

        if not got_button_press or self.output_queue.state != PlayingState.PLAY:
            return False

        sorted_notes = self.output_queue.queue.peekn(8)
        found_time = None
        played_missed_note = False

        # Look if there's a note that's close enough to the button press
        for note in sorted_notes:
            # Skip notes the user has already hit or can't hit
            if note.was_hit or not note.split_note:
                continue
            # Only look at notes that are close enough
            elif note.timestamp - relative_time > 0.333:
                break
            # If we found a note that's close enough, play it
            elif found_time is None or abs(note.timestamp - found_time) < 0.1:
                if found_time is None:
                    found_time = note.timestamp

                    self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.HIT_NOTE, note.timestamp - relative_time)))

                if abs(note.timestamp - relative_time) < 0.15:
                    # If they're close enough, make it *sound* perfect by letting it play normally
                    note.play_note = True
                    note.was_hit = True
                else:
                    # Otherwise make them hear the pain of their bad timing
                    note.was_hit = True
                    self.output_queue._send_midi_event(note)

        # If the user missed a note but it's still close enough, play it
        if len(self.playing_missed_notes) > 0:
            for event in self.playing_missed_notes:
                if relative_time - event.timestamp < 0.333:
                    played_missed_note = True
                    event.timestamp = relative_time
                    self.output_queue._send_midi_event(event)
                else:
                    self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.MISSED_NOTE, note.timestamp - relative_time)))

            if played_missed_note:
                self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.HIT_NOTE, note.timestamp - relative_time)))

            self.playing_missed_notes = []

    def on_note_output(self, midiEvent: MidiEvent):
        # Remove any missed notes that are now done completely
        if midiEvent.event.type == "note_off":
            self.playing_missed_notes = list(filter(lambda x: x.event.note != midiEvent.event.note, self.playing_missed_notes))

        if midiEvent.split_note and not midiEvent.play_note:
            self.playing_missed_notes += [midiEvent]