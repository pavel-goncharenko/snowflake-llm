# Snowflake LLM

OpenAI client integration with Snowflake Cortex.

## Snowflake setup

Enable Network policies in your Demo account for enabling PATs:

```sql
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';

CREATE DATABASE SETTINGS;
CREATE SCHEMA SETTINGS.MAIN;
USE SCHEMA SETTINGS.MAIN;
CREATE NETWORK RULE allow_access_rule
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('0.0.0.0/0');
CREATE NETWORK POLICY public_network_policy
  ALLOWED_NETWORK_RULE_LIST = ('allow_access_rule');
--- Only for Demo/Trial account, in PRD narrow IPs, VPCs, or only user network policy should be used:
ALTER ACCOUNT SET NETWORK_POLICY = public_network_policy;
```

Generate and save the token:

```sql
ALTER USER ADD PROGRAMMATIC ACCESS TOKEN demo_token;
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env`:
```env
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_PAT=your_token
```

## 1. Run Cortex example:

```bash
python cortex_example.py
```

## 2. Run OpenAI example:

```bash
python openai_example.py
```

## 2. Run SQL example:

```bash
python cortex_sql_example.py
```
