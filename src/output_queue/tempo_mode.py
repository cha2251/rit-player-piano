
import time
from src.common.midi_event import MidiEvent
from src.communication.messages import Message, MessageType, TempoModeMessage, TempoModeMessageType
from src.output_queue.output_comm import OutputCommSystem

class TempoMode():

    def __init__(self, output_queue):
        self.output_queue = output_queue
        self.comm_system = OutputCommSystem()

        self.playing_missed_notes = []
        self.playing_hit_notes = []

    def update(self, button_events: list, relative_time: float):
        if len(button_events) == 0:
            return

        sorted_notes = self.output_queue.queue.peekn(8)

        found_time = None

        for note in sorted_notes:
            if note.timestamp - relative_time > 0.333:
                break
            elif not note.was_hit and note.split_note and (found_time is None or abs(note.timestamp - found_time) < 0.1):
                if found_time is None:
                    found_time = note.timestamp

                    self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.HIT_NOTE, note.timestamp - relative_time)))

                if abs(note.timestamp - relative_time) < 0.15:
                    # If they're close enough, make it *sound* perfect by letting it play normally
                    note.should_play = True
                    note.was_hit = True
                else:
                    # Otherwise make them hear the pain of their bad timing
                    note.was_hit = True
                    self.output_queue._send_midi_event(note)
            elif (found_time is not None and abs(note.timestamp - found_time) >= 0.1):
                break

        if found_time is None and len(self.playing_missed_notes) > 0:
            played_missed_note = False

            for event in self.playing_missed_notes:
                if relative_time - event.timestamp < 0.333:
                    played_missed_note = True
                    event.timestamp = relative_time
                    self.output_queue._send_midi_event(event)
                else:
                    self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.MISSED_NOTE, note.timestamp - relative_time)))

            if played_missed_note:
                self.comm_system.send(Message(MessageType.TEMPO_MODE_UPDATE, TempoModeMessage(TempoModeMessageType.HIT_NOTE, note.timestamp - relative_time)))

            self.last_note_time_played = time.time()
            self.last_note_timestamp = relative_time
            self.playing_missed_notes = []

    def on_note_output(self, midiEvent: MidiEvent, relative_time: float):
        if midiEvent.event.type == "note_off":
            self.playing_missed_notes = list(filter(lambda x: x.event.note != midiEvent.event.note, self.playing_missed_notes))

        if midiEvent.split_note and midiEvent.should_play:
            pass # print("HIT THIS")
        elif midiEvent.split_note and not midiEvent.should_play:
            self.playing_missed_notes += [midiEvent]