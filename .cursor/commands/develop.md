# Development Process Guide

## Overview

This document outlines the development workflow and best practices for the AI-Podcast project. Following this process ensures consistency, quality, and proper documentation throughout the development lifecycle.

---

## Starting a New Task

Before beginning any development work, follow these steps:

### 1. Consult Project Requirements

Review the comprehensive requirements in the `documentation/` folder:

- **[PRD.MD](./PRD.MD)**: Product Requirements Document
  - Understand the product vision, user stories, and functional requirements
  - Review the target personas and conversation flow
  - Check success criteria and acceptance criteria
  
- **[TECHNICAL_SPECS.MD](./TECHNICAL_SPECS.MD)**: Technical Specifications
  - Review technical architecture and design patterns
  - Understand the ADK agent structure
  - Check implementation phases and technical requirements
  - Review data models, API specifications, and code examples
  - Understand the persona configuration system

### 2. Review Development History

Check `project_mangement/PROGRESS.MD` to understand:
- What has been completed previously
- Current state of the application
- Any ongoing issues or blockers
- Lessons learned from past development
- Dependencies between completed tasks

### 3. Plan Your Work

Based on the requirements and progress:
- Identify the specific task or feature to implement
- Determine which phase it belongs to (Phase 1, 2, or 3)
- Check for any prerequisites or dependencies
- Understand acceptance criteria
- Identify potential risks or challenges

---

## During Development

### Best Practices

1. **Use `.venv` Virtual Environment**: Always use `.venv` as the virtual environment for this project
   - Create with: `python3 -m venv .venv`
   - Activate with: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
   - Install dependencies: `pip install -r requirements.txt`

2. **Follow ADK Structure**: Use Google ADK's recommended folder structure
   - Each agent in its own folder with `__init__.py` and `agent.py`
   - Keep backend, database, and UI components separated

3. **Maintain Code Quality**:
   - Follow PEP 8 Python style guidelines
   - Add docstrings to functions and classes
   - Write clear, self-documenting code
   - Include type hints where appropriate

4. **Test as You Go**:
   - Write unit tests for new functions/classes
   - Test agent behavior with different inputs
   - Verify persona configurations load correctly
   - Test error handling scenarios

5. **Document Changes**:
   - Update inline code comments
   - Update README if user-facing changes occur
   - Note any configuration changes needed

6. **Version Control**:
   - Make frequent, atomic commits
   - Write clear commit messages
   - Create feature branches for significant changes

---

## Completing a Task

When you finish implementing a feature or task:

### 1. Verify Completion

- [ ] All acceptance criteria met
- [ ] Code passes linting (PEP 8)
- [ ] Unit tests written and passing
- [ ] Integration tests passing (if applicable)
- [ ] Manual testing completed successfully
- [ ] Error handling implemented
- [ ] Documentation updated

### 2. Document in PROGRESS.MD

Append a concise summary to `project_mangement/PROGRESS.MD` following this format:

```markdown
## [Date] - [Task Name]

**Phase**: [Phase 1/2/3]

**Summary**: Brief 2-3 sentence description of what was accomplished and why it matters. Do NOT include testing information.

---
```

### Example Entry:

```markdown
## 2025-10-02 - Initial Orchestrator Agent Implementation

**Phase**: Phase 1 - MVP

**Summary**: Implemented the core orchestrator agent that manages podcast conversation flow and coordinates between host and guest agents. Created the conversation flow logic, turn-taking algorithm for host and 2 guests, and integrated persona configuration loading from YAML files.

---
```

### 3. Keep PROGRESS.MD Succinct

- Keep entries to just 2-3 sentences maximum
- Focus on **what** was accomplished and **why** it matters
- **Do NOT include testing information** (testing details belong in commit messages)
- Highlight **user-facing changes** and **architectural decisions**
- Note **blockers resolved** and **lessons learned** only if significant

---

## Working with Personas

When implementing or modifying persona-related features:

1. **Review Persona Specs**: Check `TECHNICAL_SPECS.MD` sections on persona configuration
2. **Test Multiple Domains**: Verify changes work with technology, sports, and business persona sets
3. **Validate Configurations**: Ensure YAML files are properly formatted
4. **Check Distinctiveness**: Verify personas maintain unique voices

---

## Troubleshooting

If you encounter issues:

1. **Check Documentation First**: Review `TECHNICAL_SPECS.MD` troubleshooting section
2. **Review PROGRESS.MD**: See if similar issues were encountered before
3. **Check Logs**: Review application logs for error details
4. **Test in Isolation**: Create minimal test case to reproduce issue
5. **Document Solution**: Add resolution to PROGRESS.MD for future reference

---

## Communication

### For Team Members

- Update PROGRESS.MD regularly (at least once per completed task)
- Note any blockers or dependencies in PROGRESS.MD
- Communicate breaking changes immediately
- Share learnings and optimizations

### For Future Developers

- Write clear, descriptive commit messages
- Document "why" decisions were made in code comments
- Keep PROGRESS.MD as a historical record
- Update technical documentation for architectural changes

---

## Quality Checklist

Before marking any task as complete:

- [ ] Code follows project structure in `TECHNICAL_SPECS.MD`
- [ ] All tests passing (`pytest`)
- [ ] Linting passes (PEP 8 compliant)
- [ ] Persona configurations work correctly (if applicable)
- [ ] Error handling implemented
- [ ] User experience tested manually
- [ ] PROGRESS.MD updated with task summary
- [ ] Git commits are clean and well-messaged

---

## File Organization Reference

```
ai-podcast/
├── documentation/           # All project documentation
│   ├── PRD.MD              # Product requirements (READ FIRST)
│   ├── TECHNICAL_SPECS.MD  # Technical specs (READ FIRST)
│   └── PROCESS.MD          # This file
├── project_mangement/
│   └── PROGRESS.MD         # Development history (READ & UPDATE)
├── backend/                # Python backend code
│   ├── agents/             # ADK agents (orchestrator, host, guests)
│   ├── persona/            # Persona management system
│   ├── models/             # Data models
│   └── main.py             # Entry point
├── personas/               # Persona YAML configurations
│   ├── technology.yaml
│   ├── sports.yaml
│   └── business.yaml
├── tests/                  # Test suite
└── requirements.txt        # Dependencies
```

---

## Quick Reference Commands

```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows

# Run tests
pytest

# Run application
python backend/main.py

# Run with ADK
cd backend/agents
adk run orchestrator

# Check code style
flake8 backend/

# Format code
black backend/
```

---

## Remember

- **Requirements First**: Always check PRD.MD and TECHNICAL_SPECS.MD before coding
- **History Matters**: Review PROGRESS.MD to learn from past work
- **Document Progress**: Update PROGRESS.MD after completing tasks
- **Quality Over Speed**: Ensure tests pass and code is clean
- **Keep it Succinct**: PROGRESS.MD entries should be brief and actionable

---

*This process ensures consistent, high-quality development and maintains institutional knowledge for the AI-Podcast project.*

