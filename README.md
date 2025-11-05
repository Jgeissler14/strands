# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages (version 0.1.21 or later)
pip install "bedrock-agentcore-starter-toolkit>=0.1.21" strands-agents strands-agents-tools boto3

# Create the Agentcore Agent
agentcore configure -e team_lead.py

 1. Execution Role: Press Enter to auto-create or provide existing role ARN/name
 2. ECR Repository: Press Enter to auto-create or provide existing ECR URI
 3. Requirements File: Confirm the detected requirements.txt file or specify a different path 
 4. OAuth Configuration: Configure OAuth authorizer? (yes/no) - Type `no` for this tutorial
 5. Request Header Allowlist: Configure request header allowlist? (yes/no) - Type `no` for this tutorial
 6. Memory Configuration:
    - If existing memories found: Choose from list or press Enter to create new
    - If creating new: Enable long-term memory extraction? (yes/no) - Type `yes` for this tutorial
    - Note: Short-term memory is always enabled by default
    - Type `s` to skip memory setup