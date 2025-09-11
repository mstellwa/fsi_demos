# Documentation - Frost Markets Intelligence Demo

This folder contains comprehensive documentation for setting up and delivering the Frost Markets Intelligence Snowflake AI demo.

## 📚 Documentation Overview

### 🔧 [Agent Setup Instructions](agent_setup_instructions.md)
**Purpose**: Step-by-step guide for configuring Snowflake Intelligence agents  
**Audience**: Technical users setting up the demo  
**Contents**:
- Detailed agent configuration for Snowsight
- Tool setup and validation
- Troubleshooting common issues
- Test queries for validation

### 🎭 [Demo Script](demo_script.md)  
**Purpose**: Complete presentation script for client demos  
**Audience**: Sales engineers and demo presenters  
**Contents**:
- 30-45 minute modular demo script
- Business context and value propositions  
- Question flows and expected responses
- Advanced demo techniques and recovery strategies

## 🎯 Quick Start for Demo Presenters

1. **Setup**: Follow main [README.md](../README.md) to build demo environment
2. **Configure**: Use [Agent Setup Instructions](agent_setup_instructions.md) to create agents
3. **Practice**: Review [Demo Script](demo_script.md) and practice scenarios
4. **Deliver**: Use modular 15-minute segments based on client needs

## 📋 Demo Preparation Checklist

**Technical Setup** (30-45 minutes):
- [ ] Run `python setup.py --mode=full`
- [ ] Configure agents using setup instructions
- [ ] Test all demo queries
- [ ] Verify search services are indexed

**Presentation Prep** (15-30 minutes):
- [ ] Review demo script for your specific scenarios
- [ ] Customize talking points for client's industry/role
- [ ] Prepare backup queries and recovery strategies
- [ ] Test network connectivity and Snowsight access

## 🎬 Demo Scenarios

### Scenario 1: Earnings Analysis (15 minutes)
**Business Value**: 50-75% reduction in earnings analysis time  
**Key Features**: Cortex Analyst + Search, automated beat/miss analysis  
**Audience**: Equity research analysts, research managers

### Scenario 2: Thematic Research (15 minutes)  
**Business Value**: Accelerated discovery of investment themes  
**Key Features**: Alternative data analysis, cross-sector insights  
**Audience**: Research analysts, portfolio managers

## 🔗 Related Resources

- **Main Setup**: [../README.md](../README.md)
- **Configuration**: [../config.py](../config.py)  
- **Agent Templates**: [../src/ai_components/agents.py](../src/ai_components/agents.py)
- **Troubleshooting**: [../README.md#troubleshooting](../README.md#troubleshooting)

## 💡 Pro Tips

**For Technical Audiences**: 
- Show underlying SQL queries and semantic view architecture
- Demonstrate data lineage and governance capabilities
- Discuss scaling and integration patterns

**For Business Audiences**:
- Focus on workflow transformation and time savings  
- Emphasize professional output quality
- Connect features to specific business pain points

**For Executive Audiences**:
- Lead with ROI metrics and competitive advantages
- Show end-to-end business value
- Address strategic technology vision

---

*Need help? Check the main [README.md](../README.md) for additional support or troubleshooting guidance.*
