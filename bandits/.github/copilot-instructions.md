# Bandits Animation Project - AI Coding Guidelines

## Project Overview
This is a Manim-based educational animation series on multi-armed bandits, structured as 5 sequential segments. Each segment demonstrates key concepts through mathematical animations and visualizations.

## Architecture & Structure
- **Core Framework**: Manim animation library for creating mathematical visualizations
- **Segment Organization**: Each `segmentX_*.py` file contains a single `Scene` class with a `construct()` method
- **Sequential Dependencies**: Segments build on previous concepts (intro → empirical mean → concentration → suboptimality → regret)
- **Output Structure**: Videos generated in `media/videos/` subdirectories, with partial movie files for resumable rendering

## Key Patterns & Conventions

### Animation Structure
- Use `Scene.construct()` as the main animation method
- Follow consistent visual layout: header at top, main content centered, legends at bottom
- Animate step-by-step: introduce elements → perform calculations → show results → cleanup

### Visual Design
- **Arm Representation**: Blue circles with action labels (a₁, a₂, etc.) arranged horizontally
- **Color Coding**: 
  - BLUE/BLUE_E: Default arms
  - YELLOW/YELLOW_E: Active/highlighted pulls
  - GREEN/GREEN_E: Visited/optimal arms
  - PURPLE: Distribution curves
  - RED: Empirical means
- **Layout Constants**: `x_spacing = 1.7`, `radius = 0.4`, alternating label directions (UP/DOWN)

### Data & Reproducibility
- Hardcode bandit parameters (mus, sigmas) in class attributes
- Use `np.random.seed()` for deterministic animations (e.g., `SEED_PULLS = 1`)
- Generate rewards with `np.random.normal(mu, sigma)`
- Example from [segment1_bandit_intro.py](segment1_bandit_intro.py#L18-L21):
  ```python
  mus = [0.6, 0.2, 0.8, 0.4]
  sigmas = [0.15, 0.1, 0.2, 0.12]
  ```

### Mathematical Animations
- Display formulas using `MathTex` with LaTeX notation
- Animate calculations incrementally (e.g., build empirical mean step-by-step)
- Use `Transform` and `FadeTransformPieces` for smooth transitions
- Show concentration bounds with plotted curves using `Axes.plot()`

### Workflow Commands
- **Render Segment**: `manim segment1_bandit_intro.py BanditIntro -pql` (preview, quarter resolution, low quality)
- **High Quality**: `manim segment1_bandit_intro.py BanditIntro -pqh` (high quality)
- **Custom Output**: Override `config.media_dir` in script for custom paths (see [segment5_regret.py](segment5_regret.py#L5-L7))

### Dependencies & Environment
- **Virtual Environment**: Use `venv/` for isolated dependencies
- **Core Libraries**: `manim`, `numpy`
- **Import Style**: Mix of specific imports (`from manim import (Scene, Text, ...)`) and wildcard (`from manim import *`)

### File Organization
- **Source Files**: `segment*_*.py` in root directory
- **Assets**: `media/` contains generated images, LaTeX fragments, and video outputs
- **Cache**: `__pycache__/` for Python bytecode
- **Videos**: Organized by segment in `media/videos/segment*/`

## Development Tips
- Test animations incrementally - Manim rendering can be time-intensive
- Maintain consistent parameter reuse across segments (e.g., same `mus` values)
- Use partial movie files for resuming interrupted renders
- Focus on pedagogical clarity: introduce concepts visually before mathematical notation</content>
<parameter name="filePath">/Users/williamchang/Downloads/bruinml-academy/bandits/.github/copilot-instructions.md