# Next Task Suggestion Command

## Purpose

This command analyzes the AI-Podcast project to intelligently suggest the **next most impactful task** for development. It considers project requirements, current progress, and implementation dependencies to recommend a focused, actionable task that moves the project toward MVP completion.

---

## How to Use This Command

1. **Run the command**: Simply call `@suggest.md` in Cursor
2. **Review the suggestion**: Read the recommended task with its context
3. **Start development**: Use `@develop.md` to implement the suggested task

---

## Analysis Framework

This command follows a structured approach to identify the optimal next task:

### Step 1: Review Project Documentation

**Product Requirements (PRD.MD)**
- [ ] Identify all functional requirements (FR1-FR8)
- [ ] Review user stories and acceptance criteria
- [ ] Understand the conversation flow and user experience
- [ ] Note persona requirements and configuration system
- [ ] Check success criteria and metrics

**Technical Specifications (TECHNICAL_SPECS.MD)**
- [ ] Review system architecture and agent structure
- [ ] Check technical requirements (TR1-TR8)
- [ ] Understand data models and API specifications
- [ ] Review implementation phases (Phase 1, 2, 3)
- [ ] Check testing requirements and quality standards
- [ ] Understand persona configuration system design

### Step 2: Analyze Current Progress

**Review PROGRESS.MD**
- [ ] List all completed tasks and their phases
- [ ] Identify what's currently working
- [ ] Note any blockers or incomplete items
- [ ] Check for technical debt or follow-up work needed
- [ ] Review lessons learned from past implementations

**Examine Codebase**
- [ ] Check which agents are implemented (orchestrator, host, guests)
- [ ] Review what tools/capabilities exist
- [ ] Identify missing components
- [ ] Check for test coverage
- [ ] Look for placeholder code or TODOs

### Step 3: Identify Gaps & Dependencies

**Gap Analysis**
- What's required but not yet built?
- Which Phase 1 MVP features are missing?
- Are there incomplete implementations needing polish?
- What infrastructure or utilities are needed?

**Dependency Mapping**
- What's blocking other high-priority work?
- Which tasks have no dependencies and can start now?
- Are there prerequisites that need to be completed first?
- What foundational work will unlock multiple features?

### Step 4: Prioritize Based on Criteria

**Priority Factors** (in order of importance):

1. **MVP Criticality**: Is this required for Phase 1 MVP?
2. **Blocking Status**: Does this unblock other important work?
3. **User Impact**: Does this directly improve user experience?
4. **Foundation Building**: Does this enable multiple future features?
5. **Technical Debt**: Does this fix or prevent problems?
6. **Effort vs. Value**: Quick wins vs. high-effort tasks

**Phase Prioritization**:
- Phase 1 tasks take precedence (MVP features)
- Phase 2 tasks only if Phase 1 is complete
- Phase 3 tasks are lowest priority

---

## Task Suggestion Criteria

A good task suggestion should be:

### ✅ Well-Scoped
- **Single focus**: One clear objective, not multiple features
- **Time-bounded**: Achievable in 1-4 hours typically
- **Testable**: Clear success criteria
- **Completable**: Can be finished in one session

### ✅ Clearly Defined
- **Specific**: Exactly what needs to be built/changed
- **Bounded**: Clear start and end points
- **Actionable**: Provides enough context to begin immediately
- **Measurable**: Clear definition of "done"

### ✅ Properly Sequenced
- **Dependencies met**: Prerequisites are already complete
- **Logical order**: Follows natural implementation flow
- **Non-blocking**: Doesn't wait on external factors
- **Incremental**: Builds on existing work

### ✅ Valuable
- **MVP-focused**: Contributes to Phase 1 goals
- **User-impacting**: Improves the podcast experience
- **Foundation-building**: Enables future development
- **Risk-reducing**: Addresses technical uncertainties early

---

## Suggestion Output Format

When suggesting a task, provide:

### 1. Task Title
Clear, concise name describing the work

### 2. Phase & Priority
```
Phase: [1/2/3]
Priority: [Critical/High/Medium/Low]
Estimated Effort: [1-4 hours / 0.5-1 day / etc.]
```

### 3. Context & Rationale
- Why this task now?
- What gap does it fill?
- What does it enable?
- How does it relate to completed work?

### 4. Specific Requirements
- Detailed description of what needs to be built
- Reference to PRD functional requirements
- Reference to technical specifications
- Expected inputs and outputs

### 5. Acceptance Criteria
Clear checklist of requirements for completion:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### 6. Implementation Guidance
- Suggested approach or architecture
- Files to create or modify
- Key considerations or gotchas
- Testing approach

### 7. Dependencies
- **Requires**: What must be complete before starting
- **Enables**: What this will unlock for future work

---

## Example Task Suggestions

### Example 1: Early MVP Stage

```markdown
## Suggested Task: Implement Guest Agent #1 (Dr. Maya Chen)

**Phase**: Phase 1 - MVP  
**Priority**: Critical  
**Estimated Effort**: 2-3 hours  

### Context & Rationale
The orchestrator and host agents are now implemented. To enable actual podcast conversations, we need guest agents. Starting with Guest #1 (Dr. Maya Chen) establishes the pattern for all future guest agents and enables testing of multi-agent conversations.

### Specific Requirements
Implement the first guest agent following Google ADK conventions and the academic persona defined in PRD.MD (FR3).

**Functional Requirements**: FR3.1, FR3.2, FR3.3, FR3.4, FR3.5  
**Technical Requirements**: TR2.2, TR3.1, TR3.2

### Acceptance Criteria
- [ ] Guest agent created at `backend/agents/guest_maya/agent.py`
- [ ] Agent implements Dr. Maya Chen persona (academic, analytical, research-focused)
- [ ] Agent has tools: provide_expert_insight, respond_to_question, engage_in_discussion
- [ ] Agent integrated with orchestrator conversation flow
- [ ] Persona loads from YAML configuration file
- [ ] Agent maintains distinct voice from host

### Implementation Guidance
1. Create agent structure following the host agent pattern
2. Define academic persona with research-oriented language
3. Implement tools for various conversation contributions
4. Test integration with orchestrator turn-taking logic
5. Ensure distinct speaking style (references studies, uses qualifiers)

### Dependencies
- **Requires**: Orchestrator agent (✅ Complete), Host agent (✅ Complete)
- **Enables**: Guest #2 implementation, Full podcast conversation testing
```

### Example 2: Mid-MVP Stage

```markdown
## Suggested Task: Implement User Input Integration

**Phase**: Phase 1 - MVP  
**Priority**: High  
**Estimated Effort**: 3-4 hours  

### Context & Rationale
All agents are now implemented, but users cannot participate in conversations yet. This task enables the core interactive feature that distinguishes this from a passive podcast experience.

### Specific Requirements
Implement user participation functionality allowing users to inject comments/questions into the conversation flow (FR5).

**Functional Requirements**: FR5.1, FR5.2, FR5.3, FR5.4, FR5.5  
**Technical Requirements**: TR4.4, TR5.3

### Acceptance Criteria
- [ ] System prompts user for input at appropriate intervals
- [ ] User can provide text input or skip/continue
- [ ] Host agent acknowledges user input contextually
- [ ] Guest agents respond to user input when relevant
- [ ] Conversation direction changes based on user questions
- [ ] Exit commands ("stop", "exit", "quit") are recognized

### Implementation Guidance
1. Add user input prompt to conversation loop
2. Implement input parsing (comment vs. control command)
3. Pass user input to host agent as context
4. Update agent instructions to handle user contributions
5. Test various user input scenarios

### Dependencies
- **Requires**: All agents implemented (✅ Complete)
- **Enables**: Full interactive testing, Session control, User experience validation
```

---

## Anti-Patterns to Avoid

### ❌ Too Broad
"Implement the entire conversation system"
- **Problem**: Multiple features, unclear scope
- **Better**: "Implement turn-taking logic in orchestrator"

### ❌ Too Vague
"Make the agents better"
- **Problem**: No clear objective or success criteria
- **Better**: "Enhance host agent persona distinctiveness with 5 signature phrases"

### ❌ Wrong Priority
Suggesting Phase 2 features when Phase 1 is incomplete
- **Problem**: Skips MVP requirements
- **Better**: Focus on MVP gaps first

### ❌ Poorly Sequenced
"Add voice output" before text conversation works
- **Problem**: Builds on incomplete foundation
- **Better**: "Fix conversation flow issues" first

### ❌ Too Small
"Add one docstring to a function"
- **Problem**: Not substantial enough to be a focused task
- **Better**: Bundle with related work or skip

---


## Next Steps After Suggestion

Once you receive a task suggestion:

1. **Review & Clarify**: Ensure you understand the task requirements
2. **Use @develop.md**: Follow the development process guide
3. **Implement**: Build the feature according to specifications
4. **Test**: Verify acceptance criteria are met
5. **Document**: Update PROGRESS.MD upon completion

---

## Quick Reference

**When to use this command:**
- Starting a new development session
- Just completed a task and need the next one
- Unsure what to work on next
- Need prioritization guidance

**This command will NOT:**
- Implement the task for you (use `@develop.md` for implementation)
- Override explicit user requests for specific features
- Suggest tasks without analyzing current state first

---

*This command helps maintain focused, incremental progress toward MVP completion by providing intelligent task recommendations based on project state and requirements.*
