#!/bin/bash
	echo "Hello! Starting Sovereign Culinary Station Server..."
	echo ""

	exec /scs/.venv/bin/streamlit run src/scs/app.py --server.address=0.0.0.0
fi

