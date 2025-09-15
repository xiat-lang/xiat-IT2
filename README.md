# xiat-IT2
iteration 2

see docs.md for more?

github actions workflow
```
name: Enforce File Exit Code on Main

on:
  push:
    branches:
      - main

jobs:
  check_file_exit_code:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run script and check exit code
        run: |
          # Replace 'your_script.sh' with the actual path to your file
          # Ensure the script is executable (e.g., chmod +x your_script.sh)
          ./your_script.sh
```