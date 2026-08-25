# Test Execution Guide

Run commands from the repository root with the project virtual environment active. Using `python -m` ensures tools run from the interpreter where dependencies were installed.

## Pytest Commands

### Full suite

```powershell
python -m pytest -v
```

This runs all 20 currently collected tests under `tests/`.

### Collection only

```powershell
python -m pytest --collect-only -q
```

### Unit tests

```powershell
python -m pytest tests/unit/test_ivi_simulator.py -v
```

### CAN adapter tests

```powershell
python -m pytest tests/test_bus_adapter.py -v
```

### AI/RAG integration tests

```powershell
python -m pytest tests/integration/test_ivi_pipieline.py -v
```

### Individual cases

```powershell
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_play_music -v
python -m pytest tests/test_bus_adapter.py::TestCANBusAdapter::test_parse_response_valid -v
python -m pytest tests/integration/test_ivi_pipieline.py::test_rag_query -v
```

### Marker filters

```powershell
python -m pytest -m ai -v
python -m pytest -m cockpit -v
python -m pytest -m bus -v
python -m pytest -m smoke -v
```

Available markers are `smoke`, `cockpit`, `ai`, `bus`, and `slow`.

## Pytest Case Inventory

| File | Cases |
| --- | --- |
| `tests/integration/test_ivi_pipieline.py` | `test_requirement_parsing`, `test_case_generation`, `test_rag_query` |
| `tests/test_bus_adapter.py` | `test_parse_response_valid`, `test_parse_response_max`, `test_parse_response_insufficient_data`, `test_send_signal` |
| `tests/unit/test_ivi_simulator.py` | Volume parameterized cases, invalid-volume cases, valid-volume cases, boundary cases, `test_play_music`, `test_bus_message_on_volume_change` |

The parameterized groups expand to 20 collected test instances.

### Every pytest test function

```powershell
python -m pytest tests/integration/test_ivi_pipieline.py::test_requirement_parsing -v
python -m pytest tests/integration/test_ivi_pipieline.py::test_case_generation -v
python -m pytest tests/integration/test_ivi_pipieline.py::test_rag_query -v
python -m pytest tests/test_bus_adapter.py::TestCANBusAdapter::test_parse_response_valid -v
python -m pytest tests/test_bus_adapter.py::TestCANBusAdapter::test_parse_response_max -v
python -m pytest tests/test_bus_adapter.py::TestCANBusAdapter::test_parse_response_insufficient_data -v
python -m pytest tests/test_bus_adapter.py::TestCANBusAdapter::test_send_signal -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_volume_parametrized -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_set_volume_invalid -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_set_volume_valid -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_set_volume_boundary_min -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_set_volume_boundary_max -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_play_music -v
python -m pytest tests/unit/test_ivi_simulator.py::TestIVISimulator::test_bus_message_on_volume_change -v
```

The three effective parameterized simulator functions expand to 3, 3, and 3 cases respectively. The source currently contains two declarations with the same invalid-volume test name; Python keeps the latter declaration, so pytest collects 3 invalid-volume instances.

## Robot Framework Commands

### Full acceptance suite

```powershell
python -m robot --outputdir results tests/acceptance/
```

### Dry run and listing

```powershell
python -m robot --dryrun --outputdir results tests/acceptance/
python -m robot --dryrun --listtests tests/acceptance/
```

### Tag filters

```powershell
python -m robot --include smoke --outputdir results tests/acceptance/
python -m robot --include boundary --outputdir results tests/acceptance/
python -m robot --include negative --outputdir results tests/acceptance/
python -m robot --include regression --outputdir results tests/acceptance/
```

### Multimedia acceptance directory

```powershell
python -m robot --outputdir results tests/acceptance/multimedia/
```

### Individual Robot cases

```powershell
python -m robot --test "验证音量最小值-静音状态" --outputdir results tests/acceptance/
python -m robot --test "验证音量最大值-最大声压" --outputdir results tests/acceptance/
python -m robot --test "验证音量边界值-步进为1" --outputdir results tests/acceptance/
python -m robot --test "验证设置非法音量值应失败" --outputdir results tests/acceptance/
```

The acceptance suite is `tests/acceptance/multimedia/test_volum.robot`. Its four cases cover minimum volume/mute, maximum volume, step-size boundaries, and invalid values.

## RobotCode Alternative

When RobotCode is installed in the project environment, use its project-aware runner:

```powershell
robotcode discover tests
robotcode robot tests/acceptance/
robotcode robot -i smoke tests/acceptance/
```

The direct `python -m robot` commands above are the baseline because RobotCode is not in this repository's required dependency list.
