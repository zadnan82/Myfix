---
title: SEVDO Code Editing Guidelines
doc_id: kb:editing:rules:v1
tags: [editing, llm, behavior, format, rules]
updated_at: 2025-09-26
---

## Critical Editing Rules

When editing SEVDO files, you MUST follow these rules EXACTLY:

### Output Format Rules (CRITICAL)

1. Output ONLY the complete modified file content
2. NO explanations before the code
3. NO explanations after the code
4. NO comments or markdown
5. NO text like "Here is", "The code is", "I've updated", etc.
6. Start immediately with SEVDO code
7. End immediately after the last SEVDO token

### Content Rules

1. Keep ALL unchanged content exactly as-is
2. Only modify what the instruction specifically asks for
3. Preserve file structure and formatting
4. Preserve all whitespace and line breaks in unchanged sections
5. Never add new features unless explicitly asked

## Valid Editing Examples

### Example 1: Change Text Content

**Instruction:** "Change welcome to hello"

**Before:**
h(Welcome to My Site)
t(This is a blog about technology)
b(Read More)

**CORRECT Output:**
h(Hello to My Site)
t(This is a blog about technology)
b(Read More)

**WRONG Output (Don't do this):**
Here is the modified code:
h(Hello to My Site)
t(This is a blog about technology)
b(Read More)
I've changed "Welcome" to "Hello" as you requested.

### Example 2: Add Property to Element

**Instruction:** "Add green color to hero section"

**Before:**
mn(h(Site),m(Home,Blog,Contact))
ho(h(Welcome),t(Description),b(Click))
fl(h(Features),t(Our services))

**CORRECT Output:**
mn(h(Site),m(Home,Blog,Contact))
ho(h(Welcome),t(Description),b(Click)){color=green}
fl(h(Features),t(Our services))

**WRONG Output:**
Updated code:
mn(h(Site),m(Home,Blog,Contact))
ho(h(Welcome),t(Description),b(Click)){color=green}
fl(h(Features),t(Our services))

### Example 3: Change Multiple Properties

**Instruction:** "Change header text to 'My Blog' and add blue color"

**Before:**
ho(h(Welcome),t(Tech blog),b(Start))

**CORRECT Output:**
ho(h(My Blog),t(Tech blog),b(Start)){color=blue}

**WRONG Output:**
ho(h(My Blog),t(Tech blog),b(Start)){color=blue}
In this update, I changed the header text from "Welcome" to "My Blog" and added the color property with value blue.

## Common Mistakes to Avoid

### ❌ NEVER Do These:

1. **Adding explanations:**

   - "Here is the modified file:"
   - "I've updated the code:"
   - "The changes are:"
   - "As you can see..."

2. **Using markdown:**

   - \`\`\`sevdo
   - \`\`\`

3. **Explaining what you did:**

   - "I changed X to Y"
   - "This modification adds..."
   - "The code now includes..."

4. **Outputting only the changed part:**

   - Must output the COMPLETE file

5. **Adding comments:**
   - // Changed this
   - /_ Updated section _/

### ✅ ALWAYS Do These:

1. **Output complete file** - include all unchanged content
2. **Start with SEVDO code** - first character should be a token
3. **End with SEVDO code** - last character should be ) or }
4. **Keep formatting** - preserve line breaks and spacing
5. **Make minimal changes** - only what's requested

## SEVDO Syntax Quick Reference

### Basic Tokens

- `h(text)` = header/heading
- `t(text)` = text/paragraph
- `b(text)` = button
- `i(placeholder)` = input field

### Container Tokens

- `mn(...)` = menu/navigation
- `ho(...)` = hero section
- `fl(...)` = feature list
- `bl{...}` = blog list
- `cta(...)` = call-to-action

### Properties

- Single: `token{color=blue}`
- Multiple: `token{color=blue,size=large}`
- With content: `token(content){color=blue}`
- Example: `h(Title){color=blue,size=large}`

### Nesting

- Containers can nest: `ho(h(Header),t(Text),b(Button))`
- Properties apply to parent: `ho(...){color=green}`

## Remember

**Your ONLY job is to:**

1. Read the current file
2. Apply the requested change
3. Output the complete modified file
4. NOTHING ELSE

**Output format:**
[First token of SEVDO file]
[... rest of content ...]
[Last token of SEVDO file]

**NO TEXT before or after the SEVDO code!**
