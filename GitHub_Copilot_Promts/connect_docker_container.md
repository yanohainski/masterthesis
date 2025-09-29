---
description: New prompt created from chat session
mode: ask
model: GPT-4o (copilot)
---
<user>
Analyze this codebase to generate or update `.github/copilot-instructions.md` for guiding AI coding agents.

Focus on discovering the essential knowledge that would help an AI agents be immediately productive in this codebase. Consider aspects like:
- The "big picture" architecture that requires reading multiple files to understand - major components, service boundaries, data flows, and the "why" behind structural decisions
- Critical developer workflows (builds, tests, debugging) especially commands that aren't obvious from file inspection alone
- Project-specific conventions and patterns that differ from common practices
- Integration points, external dependencies, and cross-component communication patterns

Source existing AI conventions from `**/{.github/copilot-instructions.md,AGENT.md,AGENTS.md,CLAUDE.md,.cursorrules,.windsurfrules,.clinerules,.cursor/rules/**,.windsurf/rules/**,.clinerules/**,README.md}` (do one glob search).

Guidelines (read more at https://aka.ms/vscode-instructions-docs):
- If `.github/copilot-instructions.md` exists, merge intelligently - preserve valuable content while updating outdated sections
- Write concise, actionable instructions (~20-50 lines) using markdown structure
- Include specific examples from the codebase when describing patterns
- Avoid generic advice ("write tests", "handle errors") - focus on THIS project's specific approaches
- Document only discoverable patterns, not aspirational practices
- Reference key files/directories that exemplify important patterns

Update `.github/copilot-instructions.md` for the user, then ask for feedback on any unclear or incomplete sections to iterate.
</user>
<assistant>

</assistant>
<user>
how can i connect another docker container to an docker container network?
</user>
<assistant>
To connect another Docker container to an existing Docker container network, follow these steps:

### 1. **Identify the Docker Network**
   - First, find the name of the Docker network you want to connect to:
     ```bash
     docker network ls
     ```
   - Look for the network name in the output.

### 2. **Connect the Container to the Network**
   - Use the `docker network connect` command to attach the container to the network:
     ```bash
     docker network connect <network_name> <container_name_or_id>
     ```
   - Replace `<network_name>` with the name of the network and `<container_name_or_id>` with the name or ID of the container you want to connect.

### 3. **Verify the Connection**
   - Check if the container is now part of the network:
     ```bash
     docker network inspect <network_name>
     ```
   - Look for the container in the `Containers` section of the output.

### Example
If you have a network called `my_network` and a container named `my_container`, you can connect them like this:
```bash
docker network connect my_network my_container
```

### Notes
- If the container is already running, it will immediately gain access to the network.
- If you want to connect a container to the network at the time of creation, use the `--network` flag with `docker run`:
  ```bash
  docker run --network <network_name> <image_name>
  ```
</assistant>
<user>
how is the network of the notisent backend container called?
</user>
<assistant>
The network of the Notisent backend container is called `backend_net`.
</assistant>
<user>
7a79e4cd2749   bridge           bridge    local
b84ae4487687   host             host      local
06b84b1fcf30   none             null      local
30d21b20bbf3   notisent_local   bridge    local
</user>
<assistant>
The network of the Notisent backend container is called `backend_net`. This is defined in the docker-compose.dev.yml file under the `networks` section for the backend service. It is a bridge network created specifically for internal communication between services like backend, `redis`, `pg_search`, `voice-stt`, and others.
</assistant>