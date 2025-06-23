# MfinancesAI

MfinancesAI is a backend service designed to assist with financial management and analysis using AI-powered tools.

## Features

- Automated financial data processing
- AI-driven insights and analytics
- REST API for integration with other services
- Secure authentication and authorization

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) for fast Python package management (as an alternative to Poetry)

### Running Migration

- Create migration file migrate.sh and permissions to run:

```bash
#!/bin/bash

cd ~/your_path_project/
export OPENAI_API_KEY=open_ai_key
export OPENAI_API_ASSISTENT_KEY=open_ai_assistent
export DB_HOST=host_db
export DB_PORT=port_db
export DB_NAME=basefinancechat
export DB_USER=user_db
export DB_PASSWORD=pass_db
export DB_SSLMODE=disable

./.venv/bin/python migrate.py
```

### Running the Application

- Create runing file run.sh and permissions to run:

```bash
#!/bin/bash

cd ~/your_path_project/
export OPENAI_API_KEY=open_ai_key
export OPENAI_API_ASSISTENT_KEY=open_ai_assistent
export DB_HOST=host_db
export DB_PORT=port_db
export DB_NAME=basefinancechat
export DB_USER=user_db
export DB_PASSWORD=pass_db
export DB_SSLMODE=disable

./.venv/bin/python server.py
```
## License

This project is licensed under the MIT License.
