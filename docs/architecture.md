# Mirai AI — System Architecture

## Overview

Mirai AI is designed as an adaptive AI-powered interview coaching platform.

The architecture separates the user interface, application logic, AI components, analytics, and data persistence so that each component can evolve independently.

## High-Level Architecture

```text
User
  ↓
Streamlit UI
  ↓
Application Layer
  ↓
AI Engine
  ├── Question Generator
  ├── Answer Evaluator
  ├── Weakness Analyzer
  └── Follow-up Generator
  ↓
Analytics Layer
  ↓
SQLite Database