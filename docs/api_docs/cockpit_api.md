# Cockpit API

## IVISimulator

Import path: `src.cockpit.ivi_simulator`

### `IVISimulator()`

Creates an isolated simulator with default state:

- `volume=50`
- `music_playing=False`
- `current_track=""`
- `temperature=22.0`

The public state is available as `simulator.state`. The legacy alias `simulator.states` points to the same state object.

### `set_volume(volume: int) -> None`

Sets a volume from 0 through 100 inclusive. Values outside that range raise `ValueError`. Each successful change appends a simulated message with CAN ID `0x100` and the volume in its `data` field.

### `get_volume() -> int`

Returns the current volume.

### `play_music(track: str) -> None`

Sets `state.music_playing` to `True` and stores the supplied track in `state.current_track`.

### `get_last_bus_message() -> dict | None`

Returns the latest simulated bus message, or `None` when no message has been recorded.

### `reset() -> None`

Restores the default IVI state and clears simulated bus messages. pytest calls this through the `ivi_simulator` fixture teardown.

## CANBusAdapter

Import path: `src.cockpit.bus_adapter`

### `CANBusAdapter(channel: int = 0, bitrate: int = 500000)`

Creates a CAN adapter with the selected channel and bitrate. It starts disconnected.

### `connect() -> bool` and `disconnect() -> None`

Changes the connection state. `connect()` returns `True`.

### `send_signal(signal_id: int, value: int) -> None`

Records a transmit message. Raises `ConnectionError` when called before `connect()`.

### `parse_response(raw_bytes: bytes) -> int`

Requires at least two bytes and parses the first two bytes as a big-endian integer. Short input raises `ValueError`.

### `get_last_message() -> dict`

Returns the latest recorded CAN message or an empty dictionary when no message exists.

## AI Interfaces

`CaseGenerator.parse_requirement()` returns a dictionary with `module` and `test_points`. `generate_test_cases()` returns text case descriptions. `RAGPipeline.query()` returns dictionaries containing `source`, `content`, and `score` in Mock mode.
