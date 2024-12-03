# How to run tests

## Example

docker exec -it ghosts-pandora bash -c "cd .. && PYTHONPATH=\$(pwd)/app pytest app/tests/test_executable.py"
