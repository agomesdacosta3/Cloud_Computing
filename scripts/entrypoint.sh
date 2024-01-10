#!/bin/sh/

# Run the first script
/bin/sh ./test_app.sh

# Run the second script
/bin/sh ./test_container.sh

# Run tail command to keep the container running
tail -f /dev/null