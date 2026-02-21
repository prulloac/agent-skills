# Feature Type Classification Reference

This guide explains the 7 feature type categories used in feature documentation.

## The 7 Feature Types

### ⭐ Core Functionality
**Purpose**: Essential features that define why the product exists

- Answers "What is this product for?"
- Primary reason users install the product
- All other features support or enhance this

**Documentation focus**: What problem does it solve? Why is it important?

**Example**: Git blame overlay in git-blame-vsc

---

### 🎨 Customization
**Purpose**: Allows users to personalize behavior and appearance

- Enhances core functionality with flexibility
- Optional but valuable for power users
- Responds to different user preferences

**Documentation focus**: What can users customize? Provide configuration examples.

**Example**: Output pattern formatting in git-blame-vsc

---

### 👥 User Experience
**Purpose**: Improves usability, visual integration, and workflow efficiency

- Makes the product easier to use
- Reduces friction in common workflows
- Improves perceived performance

**Documentation focus**: How does it improve the experience? What workflows become easier?

**Example**: Theme-aware styling in git-blame-vsc

---

### ♿ Accessibility
**Purpose**: Supports users with different abilities and accessibility needs

- Enables keyboard-only navigation
- Provides color alternatives
- Supports screen readers
- Helps users with cognitive or motor abilities

**Documentation focus**: Who benefits? What accessibility standard is met?

**Example**: High-contrast color options, keyboard shortcuts

---

### 🚀 Performance
**Purpose**: Optimizes speed and resource usage

- Works invisibly in the background
- User perceives faster response times
- Enables support for larger datasets
- Reduces system resource consumption

**Documentation focus**: What is optimized? Include performance metrics if available.

**Example**: 30-second caching system in git-blame-vsc

---

### ➕ Extended Functionality
**Purpose**: Optional features that enhance the core capability

- Builds on core functionality
- Optional to use
- Adds value for specific use cases
- Could be removed without breaking core

**Documentation focus**: How does it extend the core feature? When is it useful?

**Example**: Export to multiple formats, advanced filtering

---

### 🛠️ Developer Experience
**Purpose**: Improves developer productivity and code quality

- Targets developers and engineers
- Reduces development friction
- Improves code quality
- Used during development/implementation

**Documentation focus**: How does it help developers? Setup instructions.

**Example**: API documentation, type definitions, debugging tools

---

## Quick Reference Matrix

| Type | Audience | Mandatory? | Visible to Users? | Configuration? |
|------|----------|-----------|-------------------|-----------------|
| ⭐ Core | End Users | YES | Always | Depends |
| 🎨 Customization | Power Users | NO | On-demand | Extensive |
| 👥 UX | End Users | NO | Often | Minimal |
| ♿ Accessibility | Specific Users | NO | On-demand | Varies |
| 🚀 Performance | Technical | NO | Indirect | Rarely |
| ➕ Extended | Power Users | NO | On-demand | Often |
| 🛠️ Developer | Developers | NO | Dev-time | Depends |

---

## Multi-Category Features

Some features belong to more than one category. **Classify by primary purpose**, note secondary types.

### Example 1: Theme-Aware Styling

**Primary**: User Experience  
**Secondary**: Accessibility

*Why*: Primarily improves visual integration (UX), secondarily enables high-contrast for accessibility

### Example 2: Keyboard Shortcuts

**Primary**: User Experience  
**Secondary**: Accessibility

*Why*: Primarily improves workflow efficiency (UX), secondarily enables keyboard-only navigation for motor accessibility

---

## Classification Decision Tree

When classifying a feature, ask these questions:

1. **Is it core to the product's purpose?**
   - YES → **Core Functionality** ⭐
   - NO → Continue to question 2

2. **Does it let users customize behavior/appearance?**
   - YES → **Customization** 🎨
   - NO → Continue to question 3

3. **Does it improve ease of use or workflow?**
   - YES → **User Experience** 👥
   - NO → Continue to question 4

4. **Does it support users with different abilities?**
   - YES → **Accessibility** ♿
   - NO → Continue to question 5

5. **Does it optimize speed or resources?**
   - YES → **Performance** 🚀
   - NO → Continue to question 6

6. **Is it for developers to use during development?**
   - YES → **Developer Experience** 🛠️
   - NO → **Extended Functionality** ➕

---

## Documentation Format

In each feature README, include:

```markdown
## Feature Type

**Category**: [Type name + icon]  
**Type**: [Brief description]

[1-2 sentences explaining why this category fits]
```

### Example

```markdown
## Feature Type

**Category**: User Experience 👥  
**Type**: Theme integration that improves visual consistency

This feature ensures the overlay integrates naturally with 
the user's current VS Code theme, providing better visual 
consistency and reducing eye strain through automatic 
adaptation to light/dark themes.
```

---

## How Classification Helps

1. **Users understand purpose** - Why does this feature exist?
2. **Feature discoverability** - Find related features easily
3. **Clear priorities** - Core features vs. nice-to-haves
4. **Expectation setting** - What should users expect?
5. **Product roadmap visibility** - Is the product balanced?

---

## Real-World Classifications

### git-blame-vsc Extension

| Feature | Type |
|---------|------|
| Git Blame Overlay | ⭐ Core Functionality |
| Customizable Formatting | 🎨 Customization |
| Theme-Aware Styling | 👥 UX + ♿ Accessibility |
| Overlay Management | 👥 UX + ⭐ Core |
| Performance Optimization | 🚀 Performance |

---

## Tips for Accurate Classification

✅ **Do**:
- Classify by actual purpose, not implementation
- Think from user's perspective
- Update classification if feature evolves
- Note secondary types if applicable

❌ **Don't**:
- Over-classify features (pick one primary type)
- Use technical details to decide (e.g., "it uses caching" ≠ Performance)
- Assume all users see the benefit the same way
- Forget to explain why you chose that category
